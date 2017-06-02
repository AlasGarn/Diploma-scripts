home=/home/domain/data/kirill/AB/XOP/md-qmmm-transition/scripts
cd /home/domain/data/kirill/AB/XOP/md/lom2/a5/S/md-qm-transition/prfs
for prf in `find . -name "prf*.gro"`
do
#	echo 25 | editconf -f $prf -o ${prf%.*}.pdb -n $home/geom.ndx
editconf -f $prf -o ${prf%.*}.pdb 
done
