#!/bin/bash
# Step 9 (optional): submit extended CG MD jobs (job_cg_ext.sh) for all 50
# trajectory folders; each job runs single_run.py with control_ext.cntrl.
# Run only after step 8.
cur_dir=`pwd`
for i in {0..49}
do
        cd ${cur_dir}/${i}/
        sbatch job_cg_ext.sh 
done

