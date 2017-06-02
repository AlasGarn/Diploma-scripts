#!/usr/bin/python -O
"""
  Script based on pdb2pqr to calculate the dipole moment of a protein
  It either takes a pdb or a pqr file. In the former case, it runs
  pdb2pqr using the force field selected by the user.
  If a pqr file the dipole calculation is made directly from this file.
  The dipole is calculated with origin at the charges-weighted centre
  of the protein. This is the convention when the molecule is not neutral.

  It produces a bild file that can be read by the program Chimera 
  (http://www.cgl.ucsf.edu/chimera/) to represent the dipole moment vector
  The user can select an appropriated color, or green will be used

  Much of the code to interface with pdb2pqr is actually from pdb2pqr,
  by Todd Dolinsky, Nathan A. Baker et al.

  Added some bits to deal with proteins that contain Se-Met (MSE)
  amino acids.
 
  Miguel Ortiz-Lombardia 21/03/2007
"""
import os, sys, getopt, string, re, math
from pdb import *

def usage():

    str = "\n"
    str = str + "dipole  \n"
    str = str + "\n"
    str = str + "This script takes a PDB file as input and runs pdb2pqr with basic options\n"
    str = str + "to assign atom radii and partial charges\n"
    str = str + "\t\tor\n"
    str = str + "takes a precalculated PQR file\n" 
    str = str + "\t\tand\n"
    str = str + "it computes from these the dipole moment\n"
    str = str + "and outputs a bild file that can be read in chimera\n"
    str = str + "to produce a colored arrow showing the dipole\n"
    str = str + "\nUsage: dipole.py [--pqrin | --ff=<forcefield>] [--color=<colorname>] [--scale=<factor>] <filename> <outfileroot>\n"
    str = str + "    Required Arguments:\n"
    str = str + "        <filename>     :  The path to the PDB file or an ID\n"
    str = str + "                          to obtain from the PDB archive\n"
    str = str + "        <outfileroot>  :  The desired root name for output files\n"
    str = str + "        (if a PDB file is provided:\n"
    str = str + "        <forcefield>   :  The forcefield to use - currently\n"
    str = str + "                          amber, charmm, and parse are supported.\n"
    str = str + "    Other Arguments:\n"
    str = str + "        <colorname> :  The desired color for the dipole arrow in the bild file\n"
    str = str + "        <scale>     :  Scale the magnitude of the vector by the desired factor\n"
    str = str + "\n"
    sys.stderr.write(str)
    sys.exit()


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:v", ["pqrin","ff=","color=","scale="])
    except getopt.GetoptError:
        # print help information and exit:
        usage()
        sys.exit(2)
    pqrin = False
    verbose = False
    color = "green"
    dipscale = 1
    forcefield = None
    for o, a in opts:
        if o == "-v":
            verbose = True
        if o in ("-h", "--help"):
            usage()
            sys.exit()
	if o == "--pqrin":
	    pqrin = True
	if o == "--color":
            color = string.lower(a)
	if o == "--scale":
            dipscale = float(a)
	if o == "--ff":
	    if a in ["amber","AMBER","charmm","CHARMM","parse","PARSE"]:
		forcefield = string.lower(a)
	    else:
		raise ValueError, "Invalid forcefield %s!" % a

    if len(args) != 2:
	sys.stderr.write("\nError: Incorrect number (%d) of arguments!\n" % len(args))
	usage()
	sys.exit()

    if pqrin == False and forcefield == None:
	sys.stderr.write("\nError: Either a PQR file is provided or the --pqrin option is given\n")
	usage()
	sys.exit()

    # If a pdb is given run pdb2pqr

    if pqrin == False:

	# Read and store PDB lines

	protpdb = open(args[0],'r')
	name = os.path.basename(sys.argv[0])

	rawlines = []

	while True:
	    pdbline = protpdb.readline()
	    if pdbline == '':
		break
	    try:
		rawlines.append(pdbline)
	    except:
		pass

	protpdb.close()

	# Substitute MET for MSE

	nomse = open('tmp.pdb','w')

	for line in rawlines:
	    if (re.search('HETATM',line) or re.search('ATOM',line)) and re.search(' MSE',line):
		line = re.sub('HETATM','ATOM  ',line)
		line = re.sub(' MSE',' MET',line)
		line = re.sub('SE   MET',' SD  MET',line)
		line = re.sub('   SE','    S',line)
		nomse.write(line)
	    else:
		nomse.write(line)

	nomse.close()

	os.system('pdb2pqr --ff=' + forcefield + ' tmp.pdb ' + args[1] + '.pqr')
	pqrfile = open(args[1] + '.pqr','r')
	pqrlines = pqrfile.readlines()
	pqrfile.close()
	os.remove('tmp.pdb')

    else:

	# If a pqr file was given, read it

	pqrfile = open(args[0],'r')
	pqrlines = pqrfile.readlines()
	pqrfile.close()

    # First pass to find out geometrical centre, centre of masses and centre of charges

    numatms, mwnumatms, cwnumatms, totcharge = 0, 0, 0, 0
    sumx, sumy, sumz = 0, 0, 0
    mwsumx, mwsumy, mwsumz = 0, 0, 0
    cwsumx, cwsumy, cwsumz = 0, 0, 0

    for line in pqrlines:
	record = string.strip(line[0:6])
	if record == "ATOM":
	    x = float(string.strip(line[30:38]))
	    y = float(string.strip(line[38:46]))
	    z = float(string.strip(line[46:54]))
	    numatms += 1
	    sumx += x
	    sumy += y
	    sumz += z
	    charge = float(string.strip(line[54:62]))
	    weight = float(string.strip(line[62:68]))
            totcharge += charge
	    mwnumatms += weight
	    mwsumx += x*weight
	    mwsumy += y*weight
	    mwsumz += z*weight
	    cwnumatms += abs(charge)
	    cwsumx += x*abs(charge)
	    cwsumy += y*abs(charge)
	    cwsumz += z*abs(charge)
	else:
	    pass

    c_x = sumx/numatms
    c_y = sumy/numatms
    c_z = sumz/numatms
    mwc_x = mwsumx/mwnumatms
    mwc_y = mwsumy/mwnumatms
    mwc_z = mwsumz/mwnumatms
    cwc_x = cwsumx/cwnumatms
    cwc_y = cwsumy/cwnumatms
    cwc_z = cwsumz/cwnumatms

    # Second pass to compute the dipole moment with origin as the centre of charges

    dp_x, dp_y, dp_z = 0, 0, 0

    for line in pqrlines:
	record = string.strip(line[0:6])
	if record == "ATOM":
	    x = float(string.strip(line[30:38]))
	    y = float(string.strip(line[38:46]))
	    z = float(string.strip(line[46:54]))
	    charge = float(string.strip(line[54:62]))
	    dp_x += (x-cwc_x)*charge
	    dp_y += (y-cwc_y)*charge
	    dp_z += (z-cwc_z)*charge
	else:
	    pass

    dpmag = math.sqrt(dp_x*dp_x + dp_y*dp_y + dp_z*dp_z)
    dpmag_SI = dpmag*1.6022e-19*1e-10
    dpmag_Deb = dpmag_SI/3.33564e-30

    # Write the dipole vector as a bild file for chimera
    
    bildfile = open(args[1]+'.bild','w')
    bildfile.write("!  Number of atoms: %i\n" % numatms)
    bildfile.write("!  Total charge: %8.5f\n" % totcharge)
    bildfile.write("!  Geometrical centre: %8.3f%8.3f%8.3f\n" % (c_x, c_y, c_z))
    bildfile.write("!  Centre of masses: %8.3f%8.3f%8.3f\n" % (mwc_x, mwc_y, mwc_z))
    bildfile.write("!  Centre of charges: %8.3f%8.3f%8.3f\n" % (cwc_x, cwc_y, cwc_z))
    bildfile.write("!  Dipole moment magnitude %8.3f D\n" % dpmag_Deb)
    bildfile.write("!  Dipole moment magnitude scale (down)\n")
    bildfile.write("!  by a factor of %5.2f in the arrow representation\n" % dipscale)
    bildfile.write(".color %s\n" % color)
    bildfile.write(".arrow  %8.3f  %8.3f  %8.3f  %8.3f  %8.3f  %8.3f  1 4 0.9\n" % (cwc_x, cwc_y, cwc_z, dp_x/dipscale+cwc_x, dp_y/dipscale+cwc_y, dp_z/dipscale+cwc_z))
    bildfile.close()


if __name__ == "__main__":
    main()