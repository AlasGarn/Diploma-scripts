# color atoms based on their distance from a point
# returns the length of the distance between atom A and atom B
 
diff_len = lambda x,y : math.sqrt((x[0]-y[0])*(x[0]-y[0]) + (x[1]-y[1])*(x[1]-y[1]) + (x[2]-y[2])*(x[2]-y[2]))
 
# fetch 1hug from the PDB
 
fetch 2D1S, async=0
 
# show it as surface
 
as cartoon
 
# create the pseudoatom at the origin
 
pseudoatom pOrig, resn slu , label=origin
 
# these are special PyMOL variables that will hold # the coordinates of 
# the atoms and the  pseudoatom
 
stored.origCoord = []
stored.distCoord = []
 
# copy the coordinates into those special variables 
 
iterate_state 1, pOrig, stored.origCoord.append((x,y,z))
iterate_state 1, 2D1S, stored.distCoord.append((x,y,z))
 
# extend origCoord to be the same length as the other
 
stored.origCoord *= len(stored.distCoord)
 
# calculate the distances
 
newB = map(lambda x,y: diff_len(x,y), stored.distCoord, stored.origCoord)
 
# put them into the b-factor of the protein
 
alter 2D1S, b=newB.pop(10)
 
# color by rainbow_rev or any other
# palette listed in "help spectrum"
 
spectrum b, yellow green blue , minimum=5,maximum=20

as spheres,resn slu
