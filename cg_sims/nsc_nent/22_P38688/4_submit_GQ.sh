#!/bin/bash
# Step 4: submit the standard GQ entanglement analysis jobs (job_GQ.sh) for
# all 50 trajectory folders to compute the G and Q metrics from the
# production trajectories.
cur_dir=`pwd`
for i in {0..49}
do
        cd ${cur_dir}/${i}/
        sbatch job_GQ.sh 
done

