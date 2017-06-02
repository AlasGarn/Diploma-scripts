#! /bin/sh
name=${1%.*}
name=${name##*/}
GMXLIB=/home/golovin/progs/share/gromacs/top/
export $GMXLIB
for a in `seq 1 40`;
do
    
    /home/golovin/progs/bin/gmx grompp -c $name".gro" -f nvt.mdp -p $name".top" -o $name"-nvt"$a".tpr" 
    /home/golovin/progs/gromacs-2016.1/bin/gmx mdrun -deffnm  $name"-nvt"$a -v -nsteps 50000 -pin on
    
done


