#!/bin/bash
# Step 4c: submit the open-variant GQ entanglement analysis jobs
# (job_GQ_open.sh) for all 50 trajectory folders.
cur_dir=`pwd`
for i in {0..49}
do
        cd ${cur_dir}/${i}/
        sbatch job_GQ_open.sh 
done

