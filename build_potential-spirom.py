#!/usr/bin/python

import numpy as np
import argparse as ag

"""
Initialization of global variables. Can be changed by hands also
"""
START, START2, START3 = -0.5, -0.5, -0.5
STOP, STOP2, STOP3 = 7.5, 7.5, 5.5
BINS = 150
STEP, STEP2, STEP3 = abs(STOP - START) / BINS, \
   abs(STOP2 - START2) / BINS, \
   abs(STOP3 - START3) / BINS
k = 1000.0 # 10^-2 kJ/A^2
tg_alpha = 0.78  # tangent of half cone angle

a0 = 4*tg_alpha # coefficient for connection

n = 1  # count for pdb output

l = 1.5 # cylinder length
r0 = 0.15 #cylider radius
Rc = 0  # cut-off radius
x0 = STOP - l #start of cylinder
x1 = x0 - 0.5 #start of smooth connection

xranges = np.arange(START, STOP + STEP, STEP)
yranges = np.arange(START2, STOP2 + STEP2, STEP2)	
zranges = np.arange(START3, STOP3 + STEP3, STEP3)

def get_args():
    parser = ag.ArgumentParser(description='Builds smooth funnel-shaped potential')
    parser.add_argument('-x', '--xcut', type = float, help = 'Cut-off distance along x axis. Areas with x < xcut are neglected', 	required = False, default = START)
    parser.add_argument('-m', '--cut', type = float, help = 'Cut-off radius. 0 - infinite (default  0)', 	required = False, default = 0)
    parser.add_argument('-t', '--tan', type = float, help = 'Tangent of half cone angle', 	required = False, default = tg_alpha)
    parser.add_argument('-g', '--bins', type = float, help = 'Number of points in grid (in one direction)', 	required = False, default = BINS)
    parser.add_argument('-a', '--alen', type = float, help = 'Cell parameter along x axis', 	required = False, default = STOP)
    parser.add_argument('-b', '--blen', type = float, help = 'Cell parameter along y axis', 	required = False, default = STOP2)
    parser.add_argument('-c', '--clen', type = float, help = 'Cell parameter along z axis', 	required = False, default = STOP3)
    parser.add_argument('-r', '--radius', type = float, help = 'Cylinder radius', 	required = False, default = r0)
    parser.add_argument('-o', '--output', type = ag.FileType('w+'), help = 'Output potential file name', required = False, default = 'external.pot')
    parser.add_argument('-p', '--pdb', type = ag.FileType('w+'), help = 'Output pdb file name', required = False, default = 'potential.pdb')
    parser.add_argument('-l', '--length', type = float, help = 'Cylinder length', required = False, default = l)
    parser.add_argument('-k', '--force', type = float, help = 'Force constant for potential', 	required = False, default = k)   
    get_args = parser.parse_args()
    args_dict = {
                'cut' : get_args.cut,
                'xcut': get_args.xcut,
                'tan' : get_args.tan,
                'bins' : get_args.bins,
                'alen' : get_args.alen,
                'blen' : get_args.blen,
                'clen' : get_args.clen,
                'output' : get_args.output,
                'radius' : get_args.radius,
                'length' : get_args.length,
                'force' : get_args.force,
                'pdb' : get_args.pdb}
    return args_dict

def sgn(x): #signum function (more exactly, Heaviside function)
	if x > 0:
		res = 1
	else:
		if x < 0:
			res = -1
		else:
			res = 1 #choose Heaviside theta1 definition
	return res

def enorm(x): #Euclid norm of n-dimensional vector
	norm = 0
	for i in x:
		norm += i**2
	norm = norm**0.5
	return norm

def R(x): #radius of potential surface
	if x < x1: #in conical area
		rd = (x0 - x)*tg_alpha + r0
	else:
		if x < x0: #in connection area
			rd = a0*(-(x0 - x)**3 + (x0 - x)**2) + r0
		else: #cylinder area
			rd = r0
	return rd

def make_force(x, y, z): #Helper. Builds force field depending on coordinates

	r = enorm([y, z])
	if x < x1: # conical area
		Fy = -1 * k * (y - (y / r) * R(x))
		Fz = -1 * k * (z - (z / r) * R(x))
		Fx = -1 * k * (r - R(x)) * tg_alpha
	else:
		if x < x0: # connection
			Fy = -1 * k * (y - (y / r) * R(x))
			Fz = -1 * k * (z - (z / r) * R(x))
			Fx = -1 * k * (r - R(x)) * -a0 * (3*(x0 - x)**2 - 2*(x0 - x))
		else: # cylinder
			Fy = -1 * k * (y - (y/r) * r0)
			Fz = -1 * k * (z - (z/r) * r0)
			Fx = 0
	return Fx, Fy, Fz

def make_pot(x): # Main logic. Builds potential in y0z plane at constant x
	pdblines = []
	potlines = []

	Rt = R(x) + Rc # there's no need to produce potential in the area the system won't ever explore

	for y0 in yranges:
		y = y0 - (STOP2 + START2) / 2.0  # set origin on the center of YOZ plane
		for z0 in zranges:
			z = z0 - (STOP3 + START3) / 2.0
			r = enorm([y, z])
			if r > Rt:
				continue
			if r < R(x):  # inside
				U, Fx, Fy, Fz = 0, 0, 0, 0
				if max(enorm([y + sgn(y)*STEP2, z]), enorm([y, z + sgn(z)*STEP3])) >= R(x): # output surface for visualizing
					pdblines.append('%-6s%5d  %-4s%-3s %1s%4d    %8.3f%8.3f%8.3f%6.2s%6.2s          %2s%2s\n'\
							  %('ATOM', 1, 'CS','CS','Z',1,\
								 x*10, y0*10, z0*10, '','','',''))
			else:
				U = 0.5 * k * (r - R(x)) ** 2

				Fx, Fy, Fz = make_force(x, y, z)
			potlines.append("%12.6lf  %12.6lf   %12.6lf  %12.6lf  %12.6lf  %12.6lf  %12.6lf\n" %
					(x, y0, z0, U, Fx, Fy, Fz))
		potlines.append('\n')
	return pdblines, potlines

def main():

	pdb = []
	pot = []

	"""
	Reinitialization of global variables. May seem unnecessary, but we are now able to access them either by command line or by hands
     """
	global Rc, START, STOP, STOP2, STOP3, BINS, STEP, STEP2, STEP3, k, tg_alpha, a0, l, r0, x0, x1, xranges, yranges, zranges

	args = get_args()
	if args['cut'] == 0:
		Rc = max(args['blen'], args['clen'])
	else:
		Rc = args['cut']

	START = args['xcut']

	STOP, STOP2, STOP3 = args['alen'], args['blen'], args['clen']
	BINS = args['bins']
	STEP, STEP2, STEP3 = abs(STOP - START) / BINS, \
   	abs(STOP2 - START2) / BINS, \
   	abs(STOP3 - START3) / BINS
	k = args['force']
	tg_alpha = args['tan']

	a0 = 4*tg_alpha
	l = args['length']
	r0 = args['radius']
	x0 = STOP - l
	x1 = x0 - 0.5

	xranges = np.arange(START, STOP + STEP, STEP)
	yranges = np.arange(START2, STOP2 + STEP2, STEP2)	
	zranges = np.arange(START3, STOP3 + STEP3, STEP3)

	for x in xranges:
		a, b = make_pot(x)
		pdb.extend(a)
		pot.extend(b)

	f = args['output']
	f.write('#! FIELDS xyz.x xyz.y xyz.z external.bias der_xyz.x der_xyz.y der_xyz.z\n')
	f.write('#! SET min_xyz.x {0}\
	        \n#! SET max_xyz.x {1}\
	        \n#! SET nbins_xyz.x {2}\
	        \n#! SET periodic_xyz.x false\n'.format(START, 	STOP, BINS))
	f.write('#! SET min_xyz.y {0}\
	        \n#! SET max_xyz.y {1}\
	        \n#! SET nbins_xyz.y {2}\
	        \n#! SET periodic_xyz.y false\n'.format(START2, STOP2, BINS))
	f.write('#! SET min_xyz.z {0}\
	        \n#! SET max_xyz.z {1}\
	        \n#! SET nbins_xyz.z {2}\
	        \n#! SET periodic_xyz.z false\n'.format(START3, STOP3, BINS))
	f.writelines(pot)
	f.close()
	f = args['pdb']
	f.writelines(pdb)
	f.close()

if __name__ == "__main__":
    main()
