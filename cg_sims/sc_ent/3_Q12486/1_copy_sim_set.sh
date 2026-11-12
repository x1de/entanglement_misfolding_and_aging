 
#!/bin/bash
# Step 1: prepare trajectory folders. Copy template/ into 50 trajectory
# folders (0-49) and replace SETINDEX with the folder index in job.sh,
# control.cntrl, job_cg_ext.sh and control_ext.cntrl.
cur_dir=`pwd`
for i in {0..49}
do
        cd ${cur_dir}
        rm -rf ${i}
        cp -r template ${i}
        sed "s/SETINDEX/${i}/g" -i ${i}/job.sh
        sed "s/SETINDEX/${i}/g" -i ${i}/control.cntrl
        sed "s/SETINDEX/${i}/g" -i ${i}/job_cg_ext.sh
        sed "s/SETINDEX/${i}/g" -i ${i}/control_ext.cntrl
# cd ${i}_*/ && qsub job.sh

done

