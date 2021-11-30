#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import mne

#Remember to rename for your own use

source_dir = '/projects/childable_jow/SemLearn_working_dir/Split/'
avg_dir = '/projects/childable_jow/SemLearn_working_dir/Grand_averages/'

# The point is to create a dictionary of lists of evoked objects, which can be used as arguments for MNE's grand 
# average function. First I set up the dictionary, while creating a list of block names to iterate over. Second 
# comes the main loop which creates the evoked objects. The third part creates the grand averages and saves them.

all_conds =     ['inc', 'con']*4
block_names =   ['block{}'.format(nr) for nr in range(1,5)]
all_blocks =    [name for pair in zip(block_names, block_names) for name in pair]
all_evk_names = ['{}_{}'.format(b, c) for b, c in zip(all_blocks, all_conds)]
empties =       [[] for nr in range(8)]
all_evokeds =   dict(zip(all_evk_names, empties))


for block_name in block_names:
    for path, dirs, files in (os.walk(source_dir)):
        for file in files:
            if block_name in file:
                block = mne.io.read_raw_fif(
                    path+'/'+file, 
                    preload=True, 
                    verbose=True
                    )
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
                    baseline=(None, 0), 
                    picks=meg_sensors, 
                    preload=True, 
                    reject=threshold, 
                    proj=True, 
                    on_missing='ignore', 
                    verbose=False
                    )
                congruent_erf = epochs['congruent'].average()
                incongruent_erf = epochs['incongruent'].average()
                all_evokeds[str(block_name)+'_con'].append(congruent_erf)
                all_evokeds[str(block_name)+'_inc'].append(incongruent_erf)
                
for block_cond in all_evokeds:
    all_evokeds[block_cond] = mne.grand_average(
        all_evokeds[block_cond], 
        interpolate_bads=True, 
        drop_bads=False
        )
    all_evokeds[block_cond].save(avg_dir+block_cond+'-ave.fif')

