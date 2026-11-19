#!/bin/bash
# Step 4b: submit the MGC-variant GQ entanglement analysis jobs
# (job_GQ_mgc.sh) for all 50 trajectory folders.
cur_dir=`pwd`
for i in {0..49}
do
        cd ${cur_dir}/${i}/
        sbatch job_GQ_mgc.sh 
done

