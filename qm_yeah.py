#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import os.path
import re
import pyparsing as pg
import numpy as np
import textwrap
from collections import OrderedDict as odict


class GRO(object):
    def __init__(self, fi, fo=None):
        self.fi = fi
        self.fo = fo

        self.header = None
        self.num = None
        self.atoms = None
        self.box = None

        self.fmt_header = '{}\n'
        self.fmt_num = '  {:d}\n'
        self.fmt_atoms = '{:5d}{:<5s}{:5s}{:5d}{:8.3f}{:8.3f}{:8.3f}\n'
        self.fmt_box = '{:10.5f}{:10.5f}{:10.5f}\n'

        self.parse()

    def parse(self, f=None):
        """Parses .gro file with coordinates"""
        if f is None:
            f = self.fi
        header = f.readline().strip()
        num = int(f.readline().strip())

        fl = pg.Word(pg.nums + '.e+-').setParseAction(lambda v: float(v[0]))

        x = fl
        y = fl
        z = fl

        parser = x + y + z

        atoms = list()
        for l in f:
            try:
                atom = self.parse_atom(l)
                atom.extend(parser.parseString(l[20:]).asList())
                atoms.append(atom)
            except pg.ParseException:
                box = parser.parseString(l).asList()

        self.header = header
        self.num = num
        self.atoms = atoms
        self.box = box

    def parse_atom(self, l):
        try:
            resi = int(l[:5])
            resn = l[5:10].strip()
            atom = l[10:15].strip()
            anum = int(l[15:20])
        except (IndexError, ValueError):
            raise pg.ParseException('Not an atom')

        return([resi, resn, atom, anum])

    def write(self, fo=None):
        """Writes .gro file with new coordinates"""
        if fo is None:
            fo = self.fo

        self.num = len(self.atoms)

        fo.write(self.fmt_header.format(self.header))
        fo.write(self.fmt_num.format(self.num))
        for i in range(self.num):
            a = self.atoms[i]
            a[3] = i + 1
            fo.write(self.fmt_atoms.format(*a))
        fo.write(self.fmt_box.format(*self.box))


class AddLinkingAtoms(object):
    def __init__(self, args):
        """Initialize class instance"""
        self.LA = 'LA'
        self.args = args


        if 'GMXLIB' in os.environ:
            self.GMXLIB = os.environ['GMXLIB']
        else:
            self.GMXLIB = '/usr/share/gromacs/top'

        self.group = None
        self.la = None
        self.la_ind = None

    def process(self):
        """Main function"""
        self.bonds2break = self.read_la_list()

        self.groups = self.read_index(self.args.input_index)
        self.group = self.select_group()

        self.gro = GRO(self.args.input_coordinates)

        self.process_topology()

        self.write_index(self.args.output_index)

        self.add_la_coordinates()
        self.gro.write(self.args.output_coordinates)

        self.clean()

    def add_la_coordinates(self):

        atoms = list()
        num = len(self.bonds2break)

        for i in range(num):

            atom = list()
            top = self.la_atoms[i]
            atom.append(top[2])  # resi
            atom.append(top[3])  # resn
            atom.append(top[4])  # aname
            atom.append(top[0])  # num

            bb = self.bonds2break[i]
            ain, ajn = bb[:2]
            ai = np.array(self.gro.atoms[ain - 1][4:])
            aj = np.array(self.gro.atoms[ajn - 1][4:])

            la = ai + (aj - ai) * self.get_ratio(*bb[:4])

            atom.extend(la)
            atoms.append(atom)
        for i in range(num):
            self.gro.atoms.insert(self.la_ind[i] - 1, atoms[i])
        for i in range(self.la_ind[-1], len(self.gro.atoms)):
            self.gro.atoms[i][0] += num
#        self.gro.atoms.extend(atoms)

    def process_topology(self, fi=None, fo=None):
        if fi is None:
            fi = self.args.input_topology
        if fo is None:
            fo = self.args.output_topology

        self.check_forcefield(fi)

        with open(os.path.join(self.ff_path, 'ffbonded.itp'), 'r') as f:
            self.btypes = self.read_bonds(f)

        self.process_header(fi, fo)

        self.check_section_name(fi, fo, 'moleculetype')
        self.process_moleculetype(fi, fo)

        self.check_section_name(fi, fo, 'atoms')
        self.atoms = self.process_atoms(fi, fo)
        self.la_ind, self.la_atoms = self.add_la_atoms(fo)

        self.check_section_name(fi, fo, 'bonds')
        self.process_bonds(fi, fo)

        self.add_section_virtual_sites2(fo)

        self.check_section_name(fi, fo, 'pairs')
        self.process_pairs(fi, fo)

        self.check_section_name(fi, fo, 'angles')
        self.process_angles(fi, fo)

        self.check_section_name(fi, fo, 'dihedrals')
        self.process_dihedrals(fi, fo)

        self.check_section_name(fi, fo, 'dihedrals')
        self.process_dihedrals(fi, fo)

        self.process_footer(fi, fo)

    def check_forcefield(self, f):
        self.ff_name = self.detect_ff(f)
        if os.path.isdir(self.ff_name):
            print 'Forcefield {} in current directory'.format(self.ff_name)
            self.ff_path = self.ff_name
        elif os.path.isdir(os.path.join(self.GMXLIB, self.ff_name)):
            print 'Forcefield {0} in {1} directory'.format(self.ff_name, self.GMXLIB)
            self.ff_path = os.path.join(self.GMXLIB, self.ff_name)

        with open(os.path.join(self.ff_path, 'atomtypes.atp'), 'r') as f:
            atypes = self.read_atomtypes(f)

        if self.LA not in atypes:
            raise TypeError('Missing {} atomtype in atomtypes.atp'.format(self.LA))

        with open(os.path.join(self.ff_path, 'ffnonbonded.itp'), 'r') as f:
            nonbonded = self.read_nonbonded(f)

        if self.LA not in nonbonded:
            raise TypeError('Missing {} atomtype in ffnonbonded.itp'.format(self.LA))

        print '\nFound {} in forcefield'.format(self.LA)

        return True

    def clean(self):
        """Close all descriptors and exit"""

        self.args.la_list.close()
        self.args.input_index.close()
        self.args.input_topology.close()
        self.args.input_coordinates.close()

        self.args.output_index.close()
        self.args.output_topology.close()
        self.args.output_coordinates.close()

    def add_section_virtual_sites2(self, fo):
        """Add section virtual_sites
        [ virtual_sites2 ]
         LA QMatom MMatom 1 X.XXX
        """

        fmt = ['{:5d}', '{:5d}', '{:5d}', '    1', '{:8.3f}', '\n']

        fo.write('\n')
        fo.write('; Linkage atoms for QM/MM\n')
        fo.write('[ virtual_sites2 ]\n')
        for i in range(len(self.la_ind)):
            site = list()
            site.append(self.la_ind[i])
            bb = self.bonds2break[i]
            site.extend(bb[:2])
            site.append(self.get_ratio(*bb[:4]))
            fo.write(' '.join(fmt).format(*site))
        fo.write('\n')

        return True

    def get_atype(self, a):
        """Returns atom type"""
        return self.atoms[a - 1][0]

    def get_ratio(self, ai, aj, atype, htype):
        new = self.btypes[(atype, htype)][1]
        old = self.btypes[(self.get_atype(ai), self.get_atype(aj))][1]
        return(new / old)

    def adjust_index(self):
        """Adjust indexes after adding of linking atoms"""
        def adjust(start, offset, v):
            if v > start:
                return v + offset
            else:
                return v
        for i in self.groups.keys():
            self.groups[i] = map(lambda x: adjust(self.la_ind[0], len(self.la_ind), x), self.groups[i])

        self.groups[self.group].extend(self.la_ind)
        self.groups['System'].extend(self.la_ind)

    def write_index(self, f):
        """Writes new .ndx file with LA being added"""
        self.adjust_index()
        for i in self.groups.keys():
            f.write('\n[ {} ]\n'.format(i))

            group = ' '.join(map(str, self.groups[i]))
            group = textwrap.fill(group, 100) + '\n'
            f.write(group)

    def process_dihedrals(self, fi, fo):
        """Comment out dihedrals of QM system"""

        group = self.groups[self.group]

        p = fi.tell()


        end = re.compile('\[')
        com = re.compile('(;|#)')

        limit = 3

        it = pg.Word(pg.nums).setParseAction(lambda v: int(v[0]))

        ai = it
        aj = it
        ak = it
        al = it
        func = it
        comment = pg.Optional(pg.Literal(';') + pg.restOfLine)

        parser = ai + aj + ak + al + func + comment

        l = fi.readline()
        while l:
            c = 0
            if end.match(l.lstrip()):
                fi.seek(p)
                break
            elif com.match(l.strip()):
                pass
            elif l.strip():
                atoms = parser.parseString(l).asList()[0:3]
                for i in atoms:
                    if i in group:
                        c += 1
                if c >= limit:
                    l = ';' + l

            fo.write(l)
            p = fi.tell()
            l = fi.readline()

        return True
        pass

    def process_angles(self, fi, fo):
        """Comment out angles of QM system"""
        group = self.groups[self.group]
        p = fi.tell()

        end = re.compile('\[')
        com = re.compile('(;|#)')

        limit = 2

        it = pg.Word(pg.nums).setParseAction(lambda v: int(v[0]))

        ai = it
        aj = it
        ak = it
        func = it
        comment = pg.Optional(pg.Literal(';') + pg.restOfLine)

        parser = ai + aj + ak + func + comment

        l = fi.readline()
        while l:
            c = 0
            if end.match(l.lstrip()):
                fi.seek(p)
                break
            elif com.match(l.strip()):
                pass
            elif l.strip():
                atoms = parser.parseString(l).asList()[0:3]
                for i in atoms:
                    if i in group:
                        c += 1
                if c >= limit:
                    l = ';' + l

            fo.write(l)
            p = fi.tell()
            l = fi.readline()

        return True

    def process_bonds(self, fi, fo):
        """Changes bondtype to 5 for all QMatoms"""
        group = self.groups[self.group]
        p = fi.tell()

        end = re.compile('\[')
        com = re.compile('(;|#)')

        fmt = ['{:5d}', '{:5d}', '{:5d}']
        limit = 2

        it = pg.Word(pg.nums).setParseAction(lambda v: int(v[0]))

        ai = it
        aj = it
        func = it
        comment = pg.Optional(pg.Literal(';') + pg.restOfLine)

        parser = ai + aj + func + comment

        l = fi.readline()
        while l:
            c = 0
            if end.match(l.lstrip()):
                fi.seek(p)
                break
            elif com.match(l.strip()):
                pass
            elif l.strip():
                atoms = parser.parseString(l).asList()[0:2]
                for i in atoms:
                    if i in group:
                        c += 1
                if c >= limit:
                    atoms.append(5)
                    l = ' '.join(fmt).format(*atoms) + ' ; QM system\n'

            fo.write(l)
            p = fi.tell()
            l = fi.readline()

        return True

    def add_la_atoms(self, f, atype=None, astart=None, rstart=None, num=None):
        """Add linking atoms to [ atoms ] section in topology"""
        if astart is None:
            astart = len(self.atoms)

        if num is None:
            num = len(self.bonds2break)

        if atype is None:
            atype = self.LA

        if rstart is None:
            rstart = self.atoms[-1][1]

        # Copied from GromacsWrapper
        fmt = ["{:6d}", "{:>10s}", "{:-6d}", "{:>6s}",
               "{:>6s}", "{:>6d}",
               "{:-10.4f}", "{:-10.3f}",
               ]
        atoms = list()
        la = list()
        f.write(';Linking atoms for QM/MM\n')
        for i in range(num):
            c = i + 1
            la.append(astart + c)
            atom = [astart + c, atype, rstart + c,
                    'XXX', atype, astart + c, 0.0, 0.0,
                    ]
            atoms.append(atom)
            astr = ' '.join(fmt).format(*atom)
            f.write(astr + '\n')

        return(la, atoms)

    def process_atoms(self, fi, fo):
        p = fi.tell()

        end = re.compile('\[')
        com = re.compile('(;|#)')

        fl = pg.Word(pg.nums + '.e+-').setParseAction(lambda v: float(v[0]))
        pr = pg.Word(pg.printables)
        it = pg.Word(pg.nums).setParseAction(lambda v: int(v[0]))

        num = it
        atype = pr
        resn = it
        resi = pr
        aname = pr
        cgnr = it
        charge = fl
        mass = fl
        comment = pg.Optional(pg.Literal(';') + pg.restOfLine)

        parser = num + atype + resn + resi + aname + cgnr + charge + mass + comment

        alist = list()
        l = fi.readline()
        while l:
            if end.match(l.lstrip()):
                fi.seek(p)
                break
            elif com.match(l.strip()):
                pass
            elif l.strip():
                alist.append(parser.parseString(l).asList()[1:8])

            fo.write(l)
            p = fi.tell()
            l = fi.readline()

        return alist

    def check_section_name(self, fi, fo, name=None):
        l = fi.readline()
        if re.match('\[ {} \]'.format(name), l):
            fo.write(l)
        else:
            raise RuntimeError('Wrong section. {} is not [ {} ]'.format(l, name))

        return True

    def process_pairs(self, fi, fo):
        """Process [ pairs ] section"""
        self.copy_stream(fi, fo)

    def process_moleculetype(self, fi, fo):
        """Process [ moleculetype ] section"""
        self.copy_stream(fi, fo)

    def process_footer(self, fi, fo):
        """Reads topology header"""
        self.copy_stream(fi, fo, ignore=True)

    def process_header(self, fi, fo):
        """Reads topology header"""
        self.copy_stream(fi, fo)

    def copy_stream(self, fi, fo, ignore=False):
        p = fi.tell()

        end = re.compile('\[')

        l = fi.readline()
        while l:
            if end.match(l.lstrip()) and not ignore:
                fi.seek(p)
                break
            else:
                pass

            fo.write(l)
            p = fi.tell()
            l = fi.readline()

        return True

    def detect_ff(self, f):
        """Reads topology and guesses forcefield path"""
        inc = re.compile('#include')
        for l in f:
            if inc.match(l.lstrip()):
                ff = re.search('"(.*\.ff)', l).group(1)
                break
        if not ff:
            raise RuntimeError('Unable to determine forcefield from topology')
        f.seek(0)
        return ff

    def read_atomtypes(self, f):
        """
        Reads atomtypes.atp and returns atoms dict
        """
        com = re.compile('(;|#)')

        atom = pg.Word(pg.printables)
        mass = pg.Word(pg.nums + '.').setParseAction(lambda v: float(v[0]))
        comment = pg.Optional(pg.Literal(';') + pg.restOfLine)

        parser = atom + mass + comment

        atypes = odict()
        for line in f:
            if com.match(line.lstrip()):
                pass
            elif line.strip():
                v = parser.parseString(line).asList()
                atypes[v[0]] = v[1]

        return atypes

    def read_nonbonded(self, f):
        """Reads ffnonbonded.itp and store parameters"""
        at = re.compile("(\[ atomtypes \]|;)")

        fl = pg.Word(pg.nums + '.e+-').setParseAction(lambda v: float(v[0]))
        atom = pg.Word(pg.printables)
        num = pg.Word(pg.nums).setParseAction(lambda v: int(v[0]))
        mass = fl
        charge = fl
        ptype = pg.Word('ABC', exact=1)
        sigma = fl
        eps = fl
        comment = pg.Optional(pg.Literal(';') + pg.restOfLine)

        parser = atom + num + mass + charge + ptype + sigma + eps + comment

        atdict = odict()
        for line in f:
            if at.match(line):
                pass
            elif line.strip():
                v = parser.parseString(line).asList()
                atdict[v[0]] = v[1:7]
        return atdict

    def read_bonds(self, f):
        """Reads [ bondtypes ] section from .itp and store parameters"""
        bt = re.compile("(\[ bondtypes \]|;)")
        end = re.compile("(\[|#)")
        bondict = odict()

        fl = pg.Word(pg.nums + '.e+-').setParseAction(lambda v: float(v[0]))
        atom = pg.Word(pg.printables)
        func = pg.Word(pg.nums).setParseAction(lambda v: int(v[0]))
        b0 = fl
        kb = fl
        comment = pg.Optional(pg.Literal(';') + pg.restOfLine)

        parser = atom + atom + func + b0 + kb + comment

        for line in f:
            if bt.match(line.lstrip()):
                pass
            elif end.match(line):
                break
            elif line.strip():
                v = parser.parseString(line).asList()
                bondict[tuple(v[:2])] = v[2:5]
                bondict[tuple(v[1::-1])] = v[2:5]
        return bondict

    def select_group(self, group=None, groups=None):

        if group is None:
            group = self.group

        if groups is None:
            groups = self.groups

        def print_groups():
            print '\n'
            print 'Groups in index file:\n'
            for i, v in enumerate(groups.keys()):
                print "Group %6d (%16s) has %5d elements" % (i, v, len(groups[v]))

        def resolve_group(groups, i):
            return groups[groups.keys()[i]]

        while (
                group is None or
                group < 0 or
                group > len(self.groups) or
                len(resolve_group(groups, group)) == 0):
                print_groups()
                group = int(raw_input("Select QM/MM group: "))

        return group.keys()[group]

    def read_index(self, f):
        """
        Read *.ndx file and store groups
        """
        groups = odict()
        g = re.compile("\[\s(.*)\s\]")
        active = None
        line = f.readline()
        while line:
            m = g.search(line)
            if m:
                active = m.group(1)
                groups[active] = list()
            elif line.strip():
                tmp = re.sub('\s+', ';', line.strip()).split(';')
                groups[active].extend(map(int, tmp))
            line = f.readline()
        return groups

    def read_la_list(self, f=None):
        """
        Reads LA list in format
        QM MM ; Optional comment
        """
        if f is None:
            f = self.args.la_list

        atype = pg.Word(pg.alphas)
        it = pg.Word(pg.nums).setParseAction(lambda v: int(v[0]))

        ai = it
        aj = it
        aitype = atype
        htype = atype

        comment = pg.Optional(pg.Literal(';') + pg.restOfLine)

        parser = ai + aj + aitype + htype + comment

        bonds = list()
        for line in f:
            bonds.append(parser.parseString(line).asList())

        if len(bonds) > 0:
            print 'Found following bonds to breake:'
            for i in bonds:
                print '{0} - {1}'.format(*i)
        else:
            raise RuntimeError('Empty linking atom list')

        return(bonds)


if __name__ == '__main__':
    import glob
    import argparse as ag
    import shutil

    def backup_output(fn):
        try:
            if os.stat(fn).st_size:
                path = os.path.dirname(fn)
                name = os.path.basename(fn)
                guess = sorted(map(
                    lambda x: int(re.sub(r'#.*\.(\d+)#', r'\1', x)),
                    glob.glob(path + "#" + name + ".*#")))
                if not guess:
                    i = 1
                else:
                    i = guess[-1]
                    if i < 99:
                        i += 1
                    else:
                        raise Exception("Too many backups")
                backup = "#" + name + '.' + str(i) + "#"
                backup = os.path.join(path, backup)
                shutil.copy(fn, backup)
                print "Back Off! I just backed up {0} to {1}".format(fn, backup)
        except OSError:
            pass

        return open(fn, 'w')

    parser = ag.ArgumentParser(
        description="""Processes GROMACS topology file (.top)
        and adds linking atoms (LA) for QM/MM.""")

    parser.add_argument('-l', '--la-list', type=ag.FileType('r'),
                        help='List of bonds to breake', required=True)
    parser.add_argument('-p', '--input-topology', type=ag.FileType('r'),
                        help='Input topology', required=True)
    parser.add_argument('-n', '--input-index', type=ag.FileType('r'),
                        help='Index file with QM/MM group', required=True)
    parser.add_argument('-c', '--input-coordinates', type=ag.FileType('r'),
                        help='Index file with QM/MM group', required=True)
    parser.add_argument('-o', '--output-topology', type=backup_output,
                        help='Output PDB file', required=True)
    parser.add_argument('-x', '--output-index', type=backup_output,
                        help='Output index file', required=True)
    parser.add_argument('-y', '--output-coordinates', type=backup_output,
                        help='Output coordinates file', required=True)
    get_args = parser.parse_args()

    add = AddLinkingAtoms(get_args)
    process = add.process()
