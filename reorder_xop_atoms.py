#!/usr/bin/pyhon2.7
import sys

ff = sys.argv[1]
order = ['P', 'O', 'O1', 'O2', 'O3', 'O4', 'N', 'H', 'N1', 'C', 'H1', 'C1', 'H2', 'C2', 'H3', 'H4', 'C3',
'H5', 'H6', 'C4', 'H7', 'H8', 'C5', 'H9', 'H10', 'C6', 'H11', 'C7', 'H12', 'H13', 'H14', 'C8',
'C9', 'H15', 'C10', 'H16', 'C11', 'C12', 'H17', 'C13', 'H18', 'C14', 'H19', 'C15', 'H20', 'C16',
'H21', 'C17', 'H22', 'C18', 'H23', 'C19']

with open(ff) as f:
    lines = f.readlines()

dic = []    
for line in lines:
	k = line.split()[2]
	dic.append([k,line])
    
dic = sorted(dic, key = lambda x: order.index(x[0]))

with open(ff,"w") as f:
	f.writelines([d[1] for d in dic])
