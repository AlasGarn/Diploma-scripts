# create an index with reacting atoms and save it as "reacting.ndx"
# the script will dump the first frame from traj with dist between reacting less than 0.235nm
for f in *xtc;
do 
	a=${f%%.*}; 
	echo $a; 
	printf "0\n\0x04" ~/progs/bin/gmx distance -n reacting.ndx -f $f -s $a".pdb" -oall; 
	echo 0 | ~/progs/bin/gmx trjconv -f $f -s $a".pdb" -o reacted-$a".pdb" -dump `awk '{if ($2 < 0.235 && NR>22){print $1; exit}}' dist.xvg `;
done
for a in reacted*pdb; do sed -i "s#XQM#XOP#g" $a; done
for a in reacted*pdb; do sed -i "/XXX/d" $a; done
