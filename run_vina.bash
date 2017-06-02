# gets xyz of cb tyr and launches vina for xopR and xopS
# 
# MAKE SURE TO HAVE CORRECT ATOM NAMES IN PDBQT, (CONSISTENT WITH YOUR FORCEFIELD)
# DON'T FORGET TO FIX HYDROGEN NAMES AFTERWARDS

for a in `find -name "a*pdbqt"`
do
	k=${a:2:-6}
	x=`grep 'CB  TYR B  33' $a | awk '{print $7}'`
	y=`grep 'CB  TYR B  33' $a | awk '{print $8}'`
	z=`grep 'CB  TYR B  33' $a | awk '{print $9}'`
	size=32
	exh=8
	printf "\n\n\n$a"
	printf "\n\n\n$x\n$y\n$z"
	printf "\n\n\n"
	mkdir $k
	vina  --log $k"R.log" --center_x $x --size_x $size --center_y $y --size_y $size --center_z $z --size_z $size --receptor $a --ligand xopR.pdbqt --exhaustiveness $exh 
	babel -ipdbqt xopR_out.pdbqt -opdb $k/xopR_out.pdb -h
	rm xopR_out.pdbqt
	
	csplit $k/xopR_out.pdb /ENDMDL/ "{*}"
	for xx in `find -name "xx*"`;
	do 
		grep "ATOM*" $xx > $k/$k"R_"${xx:5}".pdb"
	done
	
	vina  --log $k"S.log" --center_x $x --size_x $size --center_y $y --size_y $size --center_z $z --size_z $size --receptor $a --ligand xopS.pdbqt --exhaustiveness $exh 
	babel -ipdbqt xopS_out.pdbqt -opdb $k/xopS_out.pdb -h
	rm xopS_out.pdbqt
	csplit $k/xopS_out.pdb /ENDMDL/ "{*}"
	for xx in `find -name "xx*"`;
	do 
		grep "ATOM*" $xx > $k/$k"S_"${xx:5}".pdb"
	done
	rm xx*
done


