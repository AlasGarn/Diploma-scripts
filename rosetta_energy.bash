
# extract and sum up the total ligand energy (single and double)




file=${1::-4}"_breakdown.out"
/home/domain/data/prog/rosetta_bin_linux_2016.32.58837_bundle/main/source/bin/residue_energy_breakdown.static.linuxgccrelease\
	-s $1\
	-extra_res_fa /home/domain/data/kirill/AB/XOP/prepare_ligs/XOPR.params\
	-out:file:silent $file\
\
	-constraints\
	-cst_fa_file constraint.dat\
	-cst_fa_weight 1
energy=`awk '{if ($4 == 148) a+=$26}END{print a}' $file`

line=${1::-8}
printf $line"\t"$energy"\n" >> xop_energies.dat
