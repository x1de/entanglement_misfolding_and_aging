 
#!/bin/bash
# Step 8 (optional): prepare extended simulations. Copy job_cg_ext.sh and
# control_ext.cntrl from template/ into each trajectory folder and replace
# SETINDEX with the folder index. Only needed when simulations must run
# longer than the run length set in control.cntrl (1.5 microseconds).
cur_dir=`pwd`
for i in {0..49}
do
        cd ${cur_dir}
        cp template/job_cg_ext.sh ${i}/
        cp template/control_ext.cntrl ${i}/
        sed "s/SETINDEX/${i}/g" -i ${i}/job_cg_ext.sh
        sed "s/SETINDEX/${i}/g" -i ${i}/control_ext.cntrl        
# cd ${i}_*/ && qsub job.sh

done

