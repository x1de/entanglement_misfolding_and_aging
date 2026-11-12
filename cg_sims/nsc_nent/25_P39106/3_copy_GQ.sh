 
#!/bin/bash
# Step 3: prepare GQ entanglement scripts. Copy job_GQ.sh, job_GQ_mgc.sh and
# job_GQ_open.sh from template/ into each trajectory folder and replace
# SETINDEX with the folder index.
cur_dir=`pwd`
for i in {0..49}
do
        cd ${cur_dir}
        cp template/job_GQ.sh ${i}/
        cp template/job_GQ_mgc.sh ${i}/
        cp template/job_GQ_open.sh ${i}/
        sed "s/SETINDEX/${i}/g" -i ${i}/job_GQ.sh   
        sed "s/SETINDEX/${i}/g" -i ${i}/job_GQ_mgc.sh
        sed "s/SETINDEX/${i}/g" -i ${i}/job_GQ_open.sh
# cd ${i}_*/ && qsub job.sh

done

