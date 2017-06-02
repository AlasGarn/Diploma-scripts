
import numpy as np

START, START2, START3 = -0.5, 0, -0.5
STOP, STOP2, STOP3 = 12.5, 7.3, 6.7
BINS = 150
STEP, STEP2, STEP3 = abs(STOP - START) / BINS, \
   abs(STOP2 - START2) / BINS, \
   abs(STOP3 - START3) / BINS
k = 500.0 # 10^-2 kJ/A^2
tg_alfa = 0.54  # tangent of half cone angle
power = 1.     # geometry: doesn't work correctly yet (have to take dx dy dz into account)

n = 1  # count for pdb output

l = 2.6 # cylinder length
r0 = 0.1 #cylider radius

def make_cone(x): # conical part of the potential
	pdblines = []
	potlines = []
	x = 0.95*x # to make a smooth transitions between the cyl and cone
	for y0 in yranges:
		y = y0 - (STOP2 + START2) / 2.0  # center of the YOZ plane
		for z0 in zranges:
			z = z0 - (STOP3 + START3) / 2.0
			r = (y**2 + z**2)**0.5
			if r < tg_alfa * (abs(STOP - x))**power:  # inside
				U, Fx, Fy, Fz = 0, 0, 0, 0
				if r + 2*r/BINS > tg_alfa * (abs(STOP - x)): # output surface for visualizing
					pdblines.append('%-6s%5d  %-4s%-3s %1s%4d    %8.3f%8.3f%8.3f%6.2s%6.2s          %2s%2s\n'\
							  %('ATOM', 1, 'CS','CS','Z',1,\
								 (x/0.95 - l)*10, y0*10, z0*10, '','','',''))
			else:
				U = 0.5 * k * (r - tg_alfa * (STOP - x)) ** 2

				Fy = -1 * k * (y - (y / r) * tg_alfa * (STOP - x))
				# force towards cone center (normal to Fx)
				Fz = -1 * k * (z - (z / r) * tg_alfa * (STOP - x))
				# force along the cone axis (x)
				Fx = -1 * k * (r- tg_alfa * (STOP - x)) * tg_alfa
			potlines.append("%12.6lf  %12.6lf   %12.6lf  %12.6lf  %12.6lf  %12.6lf  %12.6lf\n" %
					(x/0.95 - l, y0, z0, U, Fx, Fy, Fz))
		potlines.append('\n')
	return pdblines, potlines

def make_cyl(): # cylindrical part of the potential
	pdblines = []
	potlines = []
	
	for y0 in yranges:
		y = y0 - (STOP2 + START2) / 2.0  # center of the YOZ plane
		for z0 in zranges:
			z = z0 - (STOP3 + START3) / 2.0
			r = (y**2 + z**2)**0.5
			if r < r0:  # inside
				U, Fx, Fy, Fz = 0, 0, 0, 0
				if r < r0: # output surface for visualizing
					pdblines.append('%-6s%5d  %-4s%-3s %1s%4d    %8.3f%8.3f%8.3f%6.2s%6.2s          %2s%2s\n'\
							  %('ATOM', 1, 'CS','CS','Z',1,\
								 x*10, y0*10, z0*10, '','','',''))
			else:
				U = 0.5 * k * (r - r0) ** 2
				Fy = -1 * k * (y - (y/r) * r0)
			  # force towards cone center (normal to Fx)
				Fz = -1 * k * (z - (z/r) * r0)
			  # force along the cone axis (x)
				Fx = 0
			potlines.append("%12.6lf  %12.6lf   %12.6lf  %12.6lf  %12.6lf  %12.6lf  %12.6lf\n" %
					(x, y0, z0, U, Fx, Fy, Fz))
		potlines.append('\n')
	return pdblines, potlines



xranges = np.arange(START, STOP + STEP, STEP)
yranges = np.arange(START2, STOP2 + STEP2, STEP2)
zranges = np.arange(START3, STOP3 + STEP3, STEP3)

pdb = []
pot = []

for x in xranges:
	if x > STOP - l:
		a,b = make_cyl()
		pdb.extend(a)
		pot.extend(b)
	else:
		a,b = make_cone(x+l)
		pdb.extend(a)
		pot.extend(b)

f = open('external.pot', 'w')
f.write('#! FIELDS xyz.x xyz.y xyz.z external.bias der_xyz.x der_xyz.y der_xyz.z\n')
f.write('#! SET min_xyz.x {0}\
        \n#! SET max_xyz.x {1}\
        \n#! SET nbins_xyz.x {2}\
        \n#! SET periodic_xyz.x false\n'.format(START, STOP, BINS))
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
f = open('cone.pdb', 'w')
f.writelines(pdb)
f.close()
