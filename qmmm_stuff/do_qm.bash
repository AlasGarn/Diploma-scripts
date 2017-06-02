#!/bin/bash
export PREFIX=~/progs/bin/gmx-5.0.7-nompi-double-mopac-plumed
export GMX_QM_MOPAC2012_KEYWORDS="PM7 1SCF GRADIENTS CHARGE=`cat charge.q` singlet THREADS=1"
$PREFIX grompp -f ../MDPS/eq_freeze.mdp -c conf.gro -p topol.top -o eq_freeze.tpr -n index.ndx
$PREFIX mdrun -deffnm eq_freeze -v -nt 1 &> par_eq_freeze.log  
$PREFIX grompp -f ../MDPS/equil.mdp -c eq_freeze.gro -p topol.top -o equil.tpr -n index.ndx
$PREFIX mdrun -deffnm equil -v -nt 1 &> par_md.log 
$PREFIX grompp -f ../MDPS/meta.mdp -c equil.gro -p topol.top -o meta.tpr -n index.ndx
$PREFIX mdrun -deffnm meta -v -nt 1 -plumed plumed.dat -nsteps 100000 &> par_meta.log 

