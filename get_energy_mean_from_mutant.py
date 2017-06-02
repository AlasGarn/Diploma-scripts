###
### input should be a file with space delimeted columns: "mutant name" "minimum energy"
###
### run as python get_energy_mean_from_mutant.py minima.dat


import os
import numpy as np
import re
import sys

REGEX = "(prf.*-em)" # mask to aggregate the mutants by


fl = sys.argv[1]
with open(fl) as f:
    lines = f.readlines()

recs = {}

for l in lines:
    line = l.split()
    mutant = re.search(REGEX,line[0]).group(1)
    if mutant not in recs and len(line) > 1:
        recs.update({mutant:[abs(float(line[1]))]})
    elif len(line) > 1:
        recs[mutant].append(abs(float(line[1])))
        
for a in recs.items():
	out = a[0] + "," +\
			str(int(np.mean(a[1]))) + "," +\
			str(int(np.std(a[1]))) + "," +\
			str(int(min(a[1])))
	print out 
