PREFIX="/home/domain/silwer/tmp/gromacs-5.0.4-mopac-new-plumed/build/bin/gmx"
export $PREFIX
find . ! -path . ! -path MDPS  -type "d" | parallel --gnu --env PREFIX
DIRS=`find . -name "charge.q" | xargs  dirname` 
CHARGES=`find . -name "charge.q" | xargs sed " "`


# create charges variable matching find . -type "d"



parallel --gnu --xapply --env PREFIX "
cd {1}
export GMX_QM_MOPAC2012_KEYWORDS='PM7 1SCF GRADIENTS CHARGE={2} singlet THREADS=1' 
$PREFIX grompp -f ../MDPS/eq_freeze.mdp -c conf.gro -p topol.top -o eq_freeze.tpr -n index.ndx
$PREFIX mdrun -deffnm eq_freeze -v -nt 1 -nice 10 &> par_eq_freeze.log  
$PREFIX grompp -f ../MDPS/equil.mdp -c eq_freeze.gro -p topol.top -o equil.tpr -n index.ndx
$PREFIX mdrun -deffnm equil -v -nt 1 -nice 10 &> par_md.log 
$PREFIX grompp -f ../MDPS/meta.mdp -c equil.gro -p topol.top -o meta.tpr -n index.ndx
$PREFIX mdrun -deffnm meta -v -nt 1 -plumed plumed.dat -nsteps 100000 -nice 10 &> par_meta.log 
rm ./#*
cd ..
" ::: $DIRS ::: $CHARGES

