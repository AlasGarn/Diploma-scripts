# run multiple backrubs with resfiles
# something like: ls `*parfile` | parallel --bar --gnu -j20 "bash do.bash {1}" ::: $1
# will be ok to run


# em protocol
#/home/domain/data/prog/rosetta_bin_linux_2016.32.58837_bundle/main/source/bin/relax.static.linuxgccrelease -s relax-1_0001_low.pdb -nstruct 5 -extra_res_fa /home/domain/data/kirill/AB/XOP/prepare_ligs/XOPR.params -constraints -cst_fa_file constraint.dat -overwrite -cst_fa_weight 10

base=${1::-8}
cp relaxed.pdb $base".pdb" 
NSTRUCT=5
/home/domain/data/prog/rosetta_bin_linux_2016.32.58837_bundle/main/source/bin/backrub.linuxgccrelease\
	-s $base".pdb"\
	-extra_res_fa /home/domain/data/kirill/AB/XOP/prepare_ligs/XOPR.params\
	-resfile $1\
	-overwrite\
	-backrub:ntrials 1500\
	-mc_kt 1.5\
	-nstruct $NSTRUCT\
	-sc_prob 0.5\
	-initial_pack\
	-sc_prob_withinrot 0.2\
\
	-constraints\
	-cst_fa_file constraint.dat\
	-cst_fa_weight 1\
\
	-backrub:trajectory_stride 100\
	-backrub:trajectory\
	-pivot_residues 32 33 34 35 36 37 38 39 46 47 48 49 50 51 52 53 54 57 58 59 60 61 62 64 65 68 70 96 97 98 99 100 101 102 103 104 105 106 119 137 143 144 145 146 147 148 149 150 151 152 162 163 164 165 166 167 168 169 170 171 182 187 203 204 205 206 207 208 209 210 211 212 213 214 215 216
#&> $base".log"
for a in `seq 1 $NSTRUCT`;
do
/home/domain/data/prog/rosetta_bin_linux_2016.32.58837_bundle/main/source/bin/relax.static.linuxgccrelease\
	-s $base"_"$(printf "%04d" $a)"_low.pdb"\
	-nstruct 1\
	-extra_res_fa /home/domain/data/kirill/AB/XOP/prepare_ligs/XOPR.params\
	-constraints\
	-cst_fa_file constraint.dat\
	-overwrite\
	-cst_fa_weight 1\
	-relax:bb_move false\
\
	-ex1\
	-ex2\
	-use_input_sc
done
