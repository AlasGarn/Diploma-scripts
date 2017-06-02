PYROSETTA="/home/domain/data/prog/pyrosetta"

export DYLD_LIBRARY_PATH=$PYROSETTA:$PYROSETTA/rosetta:$DYLD_LIBRARY_PATH
export LD_LIBRARY_PATH=$PYROSETTA/rosetta:$LD_LIBRARY_PATH
export PYROSETTA_DATABASE=$PYROSETTA/rosetta_database
#export PYROSETTA_DATABASE=/home/domain/anur/distr/rosetta_2015_02/rosetta_src_2015.02.57538_bundle/main/database/
export ETS_TOOLKIT=qt4



jupyter notebook --no-browser --profile="solarized-light" --ip=* --port 7003   
