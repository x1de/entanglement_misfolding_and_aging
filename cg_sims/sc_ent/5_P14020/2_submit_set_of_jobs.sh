#!/bin/bash
# Step 2: submit CG MD production jobs (job.sh) for all 50 trajectory
# folders; each job runs single_run.py with control.cntrl.
cur_dir=`pwd`
for i in {0..49}
do
        cd ${cur_dir}/${i}/
        sbatch job.sh 
done

