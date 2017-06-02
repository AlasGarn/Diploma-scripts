"""
written by demkiv
"""


import numpy as np
import sys

if len(sys.argv) != 2:
    print "First argument - name of .np file"
    exit()

grid = np.load(sys.argv[1])

def header():
    cube_file.write(" CPMD CUBE FILE.\nOUTER LOOP: X, MIDDLE LOOP: Y, INNER LOOP: Z\n")
    cube_file.write("    1 %f %f %f\n" %(-10.70000/0.529177210859, -75.10000/0.529177210859, -68.90000/0.529177210859))
    cube_file.write("  534    %f   0.000000     0.000000\n" %(0.1/0.529177210859))
    cube_file.write("  534    0.000000    %f    0.000000\n" %(0.1/0.529177210859))
    cube_file.write("  534    0.000000    0.000000    %f\n" %(0.1/0.529177210859))
    cube_file.write("    1    0.000000    %f %f %f\n" %(16.06500/0.529177210859, -48.37900/0.529177210859, -42.13700/0.529177210859))
def nucl_grid():
    i = 0
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            for z in range(grid.shape[2]):
                if i < 5:
#                    print type(float(grid[x, y, z][n])), type(number)
                    cube_file.write("%f " %(float(grid[x, y, z])/number))
                    i += 1
                elif i == 5:
                    cube_file.write("%f\n" %(float(grid[x, y, z])/number))
                    i = 0
number = float(1)
#float(12096)

cube_file = open("%s.cube" %sys.argv[1], "w")
header()
nucl_grid()
cube_file.close()
a = grid.flat[np.flatnonzero(grid)]
print np.median(a)















