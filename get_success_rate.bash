rm reacted reacted_counts all_counts counts qmr re sr 2> /dev/null
mkdir ./reacted_fess 2> /dev/null
# counts reacted COLVAR vs total
for a in `find -name "COLVAR"`; 
do  
	k=`awk 'NR>2{if ($3 < 0.17){print FILENAME ; exit;}}' $a`; 
	echo $k | grep -o prf.*-em >> reacted
	c=`awk 'NR>2{if ($3 >= 0.17){print FILENAME ; exit;}}' $a`; 
	echo $c | grep -o prf.*-em >> all
done 



sort reacted | uniq -c  > reacted_counts
sort all | uniq -c > all_counts
awk 'NR==FNR{a[$2]++; next}a[$2]>0' reacted_counts all_counts > all # a hack to get "all counts" only if the "reacted counts" are non zero
mv all all_counts

paste reacted_counts all_counts > counts

awk '{printf "%s,%.2f,%s,%s\n", $4, $1/$3, $1, $3}' counts | sort -r -t$"," -k2 > success_rate.dat



############
###
###  extract mean, minimum and sd energy
###
############

for a in `find -name "COLVAR"`; 
do
	k=`awk 'NR>5{if ($3 < 0.17){print FILENAME ; exit;}}' $a`; 
	echo $k; 
done | awk '$1 {print $0}' > reacted;

for a in `cat reacted`; 
do 
	k=${a%/*}; 
	if [ -f "./reacted_fess/${k:2}.fes" ]
	then 
		echo "${k:2} already exists - skipping sum_hills"
		continue	
	fi
	out=`basename $k`;
	/home/domain/data/prog/plumed-2.1.1/bin/plumed sum_hills --hills $k"/HILLS" --outfile ./reacted_fess/${out%.*}".fes"  1> /dev/null  
done
mkdir reacted_fess 2> /dev/null
cd reacted_fess

for a in *fes; 
do 
	awk 'NR == 6 {c = 0}; c > $2 {c=$2}; END{print FILENAME " " c}' $a; 
done > ../minima.dat
cd ..
###
### aggregate mimima by mutant
###


python ~/my_scripts/get_energy_mean_from_mutant.py minima.dat > reacted_energies.dat


# stuff for merging with success rate

# sort by name and output without 1st column
sort -k1 success_rate.dat | awk -F, '{for (i=2; i<NF; i++) printf $i ","; print $NF}' > sr 

sort -k1 reacted_energies.dat > re
paste -d, re sr > qmr
sort -k4 -r -t$"," qmr > qmmm_results.dat


#rm reacted reacted_counts all_counts counts
#rm qmr re sr
