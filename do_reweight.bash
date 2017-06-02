rm *trimmed *ready
for ecv in `ls COLVAR*`;
do
	awk 'NR > 1 && NR % 5 == 1' $ecv > $ecv".trimmed"
#	cut -d " " -f 3- $ecv".trimmed" > ${ecv::-8}".notime"
done

for ecv in `ls extra*`;
do
	awk 'NR > 2 && NR % 2 == 0' $ecv > $ecv".trimmed"
	
done

for a in `ls COLVAR*.trimmed`; 
do 
	k=${a:6:-8}; 
	paste -d' ' $a extra_CV$k".out.trimmed" > COLVAR$k".ready"; 
done

#for a in `find . -name "HILLS*"`; 
#do 
#	/home/domain/data/prog/plumed-2.1.1/bin/plumed sum_hills --hills $a --outfile fes${a:7}".dat"& 
#done
#
######################################################################################
### MAKE SURE YOU CHOOSE THE RIGHT COLUMBS FOR REWIGHTING, BIAS AND FREE ENERGY!!!!! # 
######################################################################################
##as=("s17S" "s17R")
##for k in ${as[@]};
##do
##	 cp fes$k".dat" fes0.dat;
#echo	 python ~/my_scripts/reweight.py -bsf 10 -fpref fes -nf 0 -fcol 3 -colvar COLVAR$k".ready" -rewcol 2 3 -biascol 15 -outfile fes-$k".dat";
#done
