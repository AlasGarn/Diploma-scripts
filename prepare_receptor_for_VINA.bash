export PYTHONPATH=$PYHONPATH:/usr/lib/python2.7:/usr/lib/python2.7/dist-packages
parallel "\
	python /home/domain/anur/progs/pymol/Pymol-script-repo/modules/ADT/AutoDockTools/Utilities24/prepare_receptor4.py -r {} -o {.}.pdbqt\
" ::: `find . -name "*protonated.pdb"`
