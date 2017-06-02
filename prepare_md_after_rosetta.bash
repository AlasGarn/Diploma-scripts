rm ./#*
PREFIX="/home/domain/kirill/progs/bin/gmx" 


#### CREATE TOPOLOGY ####
grep "ATOM" $1 > ${1%.*}"-temp.pdb"
grep "HETATM" $1 > ${1%.*}"-lig.pdb"
sed -i '/HD.*HIS\|HE.*HIS/d' ${1%.*}"-temp.pdb"
sed -i '/OXT/d' ${1%.*}"-temp.pdb"
sed -i '/[1,2,3]H.*VAL/d' ${1%.*}"-temp.pdb"


$PREFIX pdb2gmx -f  ${1%.*}"-temp.pdb" -ff amber99sb-ildn -renum -water tip3p -o ${1%.*}"-temp.gro" -p ${1%.*}"-temp.top" 

sed -i '/forcefield\.itp\"/a\
#include "xopR.itp"
' ${1%.*}"-temp.top" 

echo "XOP   1" >> ${1%.*}"-temp.top" 
sed -i '/xopR\.itp/a #ifdef POSRES\n#include "posre_xop.itp" \n#endif' ${1%.*}"-temp.top" 

sed -i '/bonds/i #ifdef PR \n#include "posre_1.itp" \n#endif' ${1%.*}"-temp.top" 

$PREFIX editconf -f ${1%.*}"-temp.gro" -o ${1%.*}"-compl.pdb"
sed -i "/ENDMDL/d" ${1%.*}"-compl.pdb"

python2.7 reorder_xop_atoms.py ${1%.*}"-lig.pdb" 
cat  ${1%.*}"-lig.pdb" >>  ${1%.*}"-compl.pdb"
#### SOLVATE ####

$PREFIX editconf -f ${1%.*}"-compl.pdb" -o ${1%.*}"-compl.pdb" -d 0.2 -c
$PREFIX editconf -f ${1%.*}"-compl.pdb" -o ${1%.*}"-compl.pdb" -box 6.3 6.2 4.4 -c
$PREFIX solvate -cp ${1%.*}"-compl.pdb" -p ${1%.*}"-temp.top" -o ${1%.*}"-temp.gro"

$PREFIX grompp -f ../../MDPS/em.mdp -c ${1%.*}"-temp.gro" -p ${1%.*}"-temp.top" -o ${1%.*}"-temp.tpr"

echo "15" | $PREFIX genion -s ${1%.*}"-temp.tpr" -o ${1%.*}"-temp.gro" -pname NA -pq 1 -nname CL -nq -1 -neutral -conc 0.1 -p ${1%.*}"-temp.top"
#### EM ####

$PREFIX grompp -f ../../MDPS/em.mdp -c ${1%.*}"-temp.gro" -p ${1%.*}"-temp.top" -o ${1%.*}"-temp.tpr"

$PREFIX mdrun -deffnm ${1%.*}"-temp"

mv ${1%.*}"-temp.gro" after_em/${1%.*}"-em.gro"
rm ${1%.*}"-temp"* 
rm ${1%.*}"-lig"* 
rm ${1%.*}"-compl"* 
