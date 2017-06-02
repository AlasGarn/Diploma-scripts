# must have tpr trr and xtc files with the same names together in one dir

#run this one, then the R script, finish with end.bash
home='/home/domain/data/kirill/AB/XOP/md-qmmm-transition/scripts'
find /home/domain/data/kirill/AB/XOP/md/lom2/a5/S -name "*xtc"  > list
#export PATH=$PATH:/home/domain/anur/progs/bin
while read line 
do
	cd `dirname $line`
	mkdir md-qm-transition
    /home/domain/data/prog/plumed-2.1.1/bin/plumed driver --plumed $home/driver.dat --mf_xtc $line --timestep 0.002 --trajectory-stride 250
	mv driver.out md-qm-transition
	cd md-qm-transition
	echo $nm
	awk '(NR > 4) && (NR % 2 == 0)' driver.out > DRIVER
	awk '(NR > 4) && (NR % 5 == 4)' ../COLVAR > COLVAR-trimmed
done < list

#Rscript ./get_pre_reaction_frames.R 
