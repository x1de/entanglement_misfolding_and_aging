#!/bin/bash
# Step 7: inspect fQ.dat. Print the last line of fQ.dat for each trajectory
# folder for a quick check of the native-contact fraction time series.
cur_dir=`pwd`
for i in {0..49}
do
        #cd ${cur_dir}/${i}/
        echo ${i}
       tail -n 1 ${cur_dir}/${i}/fQ.dat	
done

