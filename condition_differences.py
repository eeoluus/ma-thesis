#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import numpy as np
import mne

#Remember to rename for your own use
source_dir = '/projects/childable_jow/SemLearn_working_dir/temp/'
cdiff_dir = '/projects/childable_jow/SemLearn_working_dir/Condition_differences/'

#Calculate mean amplitude differences in the N400 time window and write them to a .csv file
for subject in os.listdir(source_dir):
    os.makedirs(cdiff_dir+subject)
    congruency_diffs = []
    for path, dirs, files in sorted(os.walk(source_dir+subject+'/')):
        for file in files:
            block = mne.io.read_raw_fif(
                path+'/'+file, 
                preload=True, 
                verbose=True)
            blockc = block.copy() 
            events = mne.find_events(
                blockc, 
                stim_channel='STI101', 
                min_duration=0.01
                )
            merged_one = mne.merge_events(
                events, 
                [311, 322, 333, 344, 355,
                 411, 422, 433, 444, 455], 
                1
                )
            merged_two = mne.merge_events(
                merged_one, 
                [312, 313, 314, 315,
                 321, 323, 324, 325,
                 331, 332, 334, 335,
                 341, 342, 343, 345,
                 351, 352, 353, 354,
                 412, 413, 414, 415,
                 421, 423, 424, 425,
                 431, 432, 434, 435,
                 441, 442, 443, 445,
                 451, 452, 453, 454], 
                2
                )
            event_dict = {
                'congruent': 1, 
                'incongruent': 2
                }
            threshold = {
                'grad': 4e-10, 
                'mag': 4e-12
                }
            meg_sensors = mne.pick_types(blockc.info)  
            epochs = mne.Epochs(
                blockc, 
                merged_two, 
                event_dict, 
                tmin=-0.2, 
                tmax=0.8, 
                baseline=(
                    None, 
                    0
                    ), 
                picks=meg_sensors, 
                preload=True, 
                reject=threshold, 
                proj=True, 
                on_missing='ignore', 
                verbose=False
                )
            congruent_erf = epochs['congruent'].average()
            incongruent_erf = epochs['incongruent'].average()
            congruency_diff = mne.combine_evoked(
                [congruent_erf, incongruent_erf], 
                weights=[1, -1]
                ).data
            sensor_averages = np.mean(
                congruency_diff[:, 500:700], 
                axis=1
                )
            congruency_diffs.append(sensor_averages)
    data = np.concatenate(
        congruency_diffs, 
        axis=0
        )
    np.savetxt(
        cdiff_dir+subject+'/'+'SemLearn_'+subject+'_diff_erf_means.csv', 
        data, 
        delimiter=','
        )

