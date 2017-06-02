# duplicates dirs "aXXRYXXLprfXX"

N=5
 
for a in `find . -name "a*prf[0-9]" -o -name "a*prf[0-9][0-9]" -type "d"`
do 
	k=$a
	for i in $(seq 2 $N)
	do 
		cp -r $k $k"_$i"
	done
done
