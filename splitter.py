#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os, mne

#Remember to rename these for your own use
source_dir = '/projects/childable_jow/SemLearn_working_dir/Filtered_and_ICA-corrected/'
split_dir = '/projects/childable_jow/SemLearn_working_dir/Split/'

#Split the data into four periods using event codes
for subject in os.listdir(source_dir):
    block_dirs = ['block1', 'block2', 'block3', 'block4']
    for name in block_dirs:
        os.makedirs(split_dir+subject+'/'+name)
    prep = mne.io.read_raw_fif(
        source_dir+subject+'/SemLearn_'+subject+'_tsss_mc/SemLearn_'+subject+'_tsss_mc.fif', 
        preload=True, 
        verbose=True
        )
    events = mne.find_events(
        prep, 
        stim_channel='STI101', 
        min_duration=0.01
        )
    
    onsets1 = mne.pick_events(
        events, 
        include=801
        ) 
    ends1 = mne.pick_events(
        events, 
        include=804
        )
    onset_t1 = onsets1[1,0] / prep.info['sfreq']
    end_t1 = ends1[0,0] / prep.info['sfreq']
    block1 = prep.copy().crop(onset_t1, end_t1)
    block1.save('/projects/childable_jow/SemLearn_working_dir/Split/'+subject+'/block1/SemLearn_'+subject+'_block1_tsss_mc.fif')
    
    onsets2 = mne.pick_events(
        events, 
        include=804
        )
    ends2 = mne.pick_events(
        events, 
        include=807
        )
    onset_t2  = onsets2[0,0] / prep.info['sfreq'] 
    end_t2 = ends2[0,0] / prep.info['sfreq']
    block2 = prep.copy().crop(
        onset_t2, 
        end_t2
        )
    block2.save('/projects/childable_jow/SemLearn_working_dir/Split/'+subject+'/block2/SemLearn_'+subject+'_block2_tsss_mc.fif')
    
    onsets3 = mne.pick_events(
        events, 
        include=807
        )
    ends3 = mne.pick_events(
        events, 
        include=809
        )
    onset_t3 = onsets3[0,0] / prep.info['sfreq']
    end_t3 = ends3[1,0] / prep.info['sfreq']
    block3 = prep.copy().crop(
        onset_t3, 
        end_t3
        )
    block3.save('/projects/childable_jow/SemLearn_working_dir/Split/'+subject+'/block3/SemLearn_'+subject+'_block3_tsss_mc.fif')
    
    onsets4 = mne.pick_events(
        events, 
        include=810
        )
    onset_t4 = onsets4[0,0] / prep.info['sfreq'] 
    end_t4 = (len(prep) - 1) / prep.info['sfreq']
    block4 = prep.copy().crop(
        onset_t4, 
        end_t4
        )
    block4.save('/projects/childable_jow/SemLearn_working_dir/Split/'+subject+'/block4/SemLearn_'+subject+'_block4_tsss_mc.fif')

