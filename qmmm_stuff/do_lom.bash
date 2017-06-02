### launches single core TASKS


TASKS=`find . -name "charge.q" | wc -l` # number of dirs -> tasks
CORES=14
NUMBER_OF_NODES=`echo "($TASKS+$CORES-1)/$CORES" | bc`

sbatch  -N $NUMBER_OF_NODES -o output.log -e error.log -p compute -t 50:00:00 ./multirun

