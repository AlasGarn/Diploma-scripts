import numpy as np
import os
import argparse
parser = argparse.ArgumentParser(description = 'Combinatorial resfile generation')
parser.add_argument("-f", help = "folder with mutants", default = os.getcwd())
parser.add_argument("-c", help = "mutant config")
parser.add_argument("-init", help = "initial resfile")
parser.add_argument("-cpu", help = "cpu count", default = 1)
parser.add_argument("-pdb", help = "initial pdb")
args = parser.parse_args()
from joblib import Parallel, delayed

RosettaSRV = '/home/domain/data/prog/rosetta_bin_linux_2016.32.58837_bundle/main/source/bin/backrub.linuxgccrelease'
absdir = os.getcwd()
pdbfile = absdir+'/'+args.pdb
paramfile = absdir+'/ECH.params'

def readconf(cfile):
    mut = {}
    for l in cfile:
        l = l.split(' ')
        pos = int(l[0])
        mut[pos] = [x for x in l[1].strip()]
    return mut

def genall(l):
    sortedv = [l[k] for k in sorted(l.keys())]
    indx = np.asarray(list(map(len,sortedv)))
    tab = np.empty((np.prod(indx),len(l.keys())), dtype=str)
    for c,i in enumerate(indx):
        tab[:,c] = np.asarray(np.prod(indx[:c])*[[ai]*np.prod(indx[c+1:]) for ai in sortedv[c]]).reshape(1,-1)
    return tab,sorted(l.keys())    
    
def mkresfile(wordl,pos,path,default):
    mutstr = ''
    name = []
    mutate = []
    for c,l in enumerate(wordl):
        if l != 'X':
            mutate.append(pos[c])
            name.append('%s%s' % (pos[c],l))
            s = '%s A PIKAA %s\n' % (pos[c],l)
            mutstr += s
    if len(name) == 0:
        return 0
    name = '_'.join(name)
    os.system('mkdir %s/%s' % (path,name))
    o = open(path+'/'+name+'/'+name+'.resfile','w')
    o.write('EX 1 EX 2\n')
    o.write('start\n')
    o.write(mutstr)
    d = open(default,'r')
    for c,l in enumerate(d):
        if int(l.split(' ')[0]) not in mutate:
            o.write(l)
    o.close()
    d.close()
    os.chdir(absdir+'/'+args.f+'/'+name)
    os.system('%s -s %s -resfile %s.resfile -extra_res_fa %s -overwrite' % (RosettaSRV,pdbfile,name,paramfile))
    os.chdir(absdir)
    return 1

with open(args.c) as fh:
    G = genall(readconf(fh))
pos = G[1]
Parallel(n_jobs = int(args.cpu))(delayed(mkresfile)(x,pos,args.f,args.init) for x in G[0])