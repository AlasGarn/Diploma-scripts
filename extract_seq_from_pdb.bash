#
# don't forget to substitute any strange residues
#
# run sort "file" | uniq > "out_file" to get uniq


sed -i 's/NVAL/VAL/g' $1 
sed -i 's/CLYS/LYS/g' $1 
seq=`cat $1 | awk '/ATOM/ && $3 == "CA" {print $4}' | tr '\n' ' ' | sed 's/ALA/A/g;s/CYS/C/g;s/ASP/D/g;s/GLU/E/g;s/PHE/F/g;s/GLY/G/g;s/HIS/H/g;s/ILE/I/g;s/LYS/K/g;s/LEU/L/g;s/MET/M/g;s/ASN/N/g;s/PRO/P/g;s/GLN/Q/g;s/ARG/R/g;s/SER/S/g;s/THR/T/g;s/VAL/V/g;s/TRP/W/g;s/TYR/Y/g' | sed 's/ //g' | sed -e '$a\'`
echo `basename ${1%%-*}` $seq
