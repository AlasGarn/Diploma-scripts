# equillibration of prf's 
export PATH=$PATH:/home/domain/anur/progs/bin
PREFIX=gmx_512_plumed_matheval

prep='/home/domain/data/kirill/AB/XOP/prepare_md'
home='/home/domain/data/kirill/AB/XOP/md-qmmm-transition/scripts'
run='a5/prepareR'
work='/home/domain/data/kirill/AB/XOP/md/lom2/a5/R/md-qm-transition/prfs'
cd $work
for prf in `find . -maxdepth 1 -name "*gro"`;
do
	dir=`basename ${prf%.*}`
	mkdir $dir
	echo $dir	
	cp $prf $dir/conf.gro
	cd $dir 
	cp $prep/$run/topol.top $prep/$run/*itp $prep/$run/index.ndx ./
	ln -s $home/amber99sb-ildn.ff $work/$dir
	#### EQUILLIBRATION ####

	$PREFIX grompp -f $prep/MDPS/pre-qm.mdp -c conf.gro -o pre-qm.tpr -p topol.top -n index.ndx
	 
	rm ./#* 
	cd ..
done
#  next - reorer-waters.ipynb


