#
# finds XOP P atom number from first gro it finds in the input dir
# cats all the gros in the dir and calculates an rdf
#
# run with parallel "bash get_rdf_from_gros.bash {}" ::: DIRS
#


cd $1
c=`ls *gro | head -n 1`
k=`grep "225XOP.*P" $c | awk '{print $3}'` 

printf "a $k\nq\n" | ~/progs/bin/gmx make_ndx -f $c
~/progs/bin/gmx trjcat -f *gro -cat
printf "24\n16\n" ~/progs/bin/gmx rdf -f trajout.xtc -norm -n index.ndx  -xvg none -rmax 1 # -cn
rm trajout.xtc
