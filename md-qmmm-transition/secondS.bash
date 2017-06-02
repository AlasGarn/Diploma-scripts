export PATH=$PATH:/home/domain/anur/progs/bin
PREFIX=gmx_512_plumed_matheval


### first we dump all prfs
cd /home/domain/data/kirill/AB/XOP/md/lom2/a5/S/md-qm-transition
mkdir prfs
echo 0 | $PREFIX trjconv -f ../cone.xtc -s ../cone.tpr -o ./prfs/prf.gro  -sep -dropunder 1 -drop pre-reaction-frames.xvg


# for some reason we get duplicate frames, so I delete every second one
for i in `seq  0 37`; do if [ $a = 0 ]; then rm prf$i.gro; ((a++)); else ((a--)); fi done


