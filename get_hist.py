import sys
import re
path = sys.argv[1]

asd = open(path,'r')
lns = asd.readlines()
asd.close()
hss = [(0,0)]

for line in lns:
    if "HIS" in line:

        his = line.split()[0]

        if hss[-1][0] != his: 
            hss.append([his,0])
            hd = False
            
        if line.split()[1] == "HD1": 
            hd = True

   
        if line.split()[1] == "HE2":
            hss[-1][1] += 1
            
            if hd == True:
                hss[-1][1] += 1


asd = open('hist.temp','w')
for h in [x[1] for x in hss[1:]]: 
    asd.write(str(h)+"\n")
asd.close()
    
