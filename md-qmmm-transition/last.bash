# move everything imto separate dirs for qm


from="/home/domain/data/kirill/AB/XOP/md/lom2/a5/S/md-qm-transition/prfs/"
dest="/home/domain/data/kirill/AB/XOP$nm/qmmm/S_lom_09.04"
mkdir $dest
cp -r qmmm_stuff/* $dest
cd $from
for f in `find . -name "*_swap.gro"` #-printf "%f\n"`
do
	nm=`dirname ${f:2}` # remove the front slash and dot
	echo $nm
  
	mkdir $dest/$nm
	cp $from/$nm/qm_qm_swap.top $dest/$nm/topol.top
	cp $from/$nm/qm_qm_swap.gro $dest/$nm/conf.gro
	cp $from/$nm/qm_qm_swap.ndx $dest/$nm/index.ndx
	cp $from/$nm/qm.q $dest/$nm/charge.q
	cp $from/$nm/qm_qm.dat $dest/$nm/plumed.dat
	cp $from/$nm/qm_qm_swap.itp $dest/$nm/posre.itp
#	rm $dest/$nm/amber99sb-ildn.ff
	ln -s /home/domain/data/kirill/AB/XOP/md-qmmm-transition/scripts/amber99sb-ildn.ff $dest/$nm
done
