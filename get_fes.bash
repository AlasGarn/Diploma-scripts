export DIRS=`find -name "a*" -type "d" | sed 's/\.\///'`

echo $DIRS

#parallel --gnu --xapply "
#
#
#cd {}
##echo HILLS{}'S'
##/home/domain/data/prog/plumed-2.1.1/bin/plumed sum_hills --outfile fes_for_prfSxy0.dat --hills HILLS{}S --kt 2.5 
##/home/domain/data/prog/plumed-2.1.1/bin/plumed sum_hills --outfile fes_for_prfRxy0.dat --hills HILLS{}R --kt 2.5 &
##python ~/my_scripts/reweight.py -fpref fes_for_prfSxy -nf 1 -biascol 4 -kt 2.5 -colvar COLVAR{}S -fcol 3 -rewcol 8 9 -bsf 10 
##mv fes_rew.dat {}'S-2dxy.fes'
##python ~/my_scripts/reweight.py -fpref fes_for_prfRxy -nf 1 -biascol 4 -kt 2.5 -colvar COLVAR{}R -fcol 3 -rewcol 8 9 -bsf 10 
##mv fes_rew.dat {}'R-2dxy.fes'         
#
#
##/home/domain/data/prog/plumed-2.1.1/bin/plumed sum_hills  --outfile fes_for_prfSyz0.dat --hills HILLS{}'S' --kt 2.5 
##/home/domain/data/prog/plumed-2.1.1/bin/plumed sum_hills  --outfile fes_for_prfRyz0.dat --hills HILLS{}'R' --kt 2.5 &
##python ~/my_scripts/reweight.py -fpref fes_for_prfSyz -nf 1 -biascol 4 -kt 2.5 -colvar COLVAR{}S -fcol 3 -rewcol 9 10 -bsf 10 
##mv fes_rew.dat {}'S-2dyz.fes'
##python ~/my_scripts/reweight.py -fpref fes_for_prfRyz -nf 1 -biascol 4 -kt 2.5 -colvar COLVAR{}R -fcol 3 -rewcol 9 10 -bsf 10
##mv fes_rew.dat {}'R-2dyz.fes'         
#
#python ~/my_scripts/reweight.py -fpref fes_for_prfSyz -nf 1 -biascol 4 -kt 2.5 -colvar COLVAR{}S -fcol 3 -rewcol 8 9 10 -bsf 10 
#mv fes_rew.dat {}'S-xyz.fes'
#python ~/my_scripts/reweight.py -fpref fes_for_prfRyz -nf 1 -biascol 4 -kt 2.5 -colvar COLVAR{}R -fcol 3 -rewcol 8 9 10 -bsf 10
#mv fes_rew.dat {}'R-xyz.fes'         
#
#" ::: $DIRS
for a in `find -name "*dyz.fes"`;
do
	cd `dirname $a`
	k=`basename $a`
	echo $k
	/home/domain/kirill/usr/bin/gnuplot -e "filename='$k'; a = 1; b = 2; c = 3" ~/my_scripts/plot_contour_yz.plg
	mv out.png ~/new_pics/${k::-4}.png
	cd ..
done
for a in `find -name "*xy.fes"`;
do
	cd `dirname $a`
	k=`basename $a`
	echo $k
	/home/domain/kirill/usr/bin/gnuplot -e "filename='$k'; a = 1; b = 2; c = 3" ~/my_scripts/plot_contour_xy.plg
	mv out.png ~/new_pics/${k::-4}.png
	cd ..
done
