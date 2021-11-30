#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import mne

def logs_to_rts(log_dir):
    """Arrange behavioral data in a log file directory as a NumPy array."""
    full_rt_data = np.zeros((4, 32, 3))
    for s in enumerate(os.listdir(log_dir)):
        if s[1] == 'desktop.ini':
            pass
        else:
            full_rt_data[:, s[0], 2] = s[1][0:3]

            data = open(log_dir+'/'+s[1])
            data_lines = [line for line in data]
            response_lines = []
            for i in range(0, len(data_lines)):
                if 'Response' in data_lines[i] and 'test' in data_lines[i-1]:
                    if 'hit' in data_lines[i-1]:
                        response_lines.append(data_lines[i])
                    else:
                        data_lines[i] = ''
                        response_lines.append(data_lines[i])
            response_lines_proper = response_lines[4:len(response_lines)]

            response_blocks = [response_lines_proper[i:i + 48] for i in range(0, len(response_lines_proper), 48)]
            for b, block in enumerate(response_blocks):
                rt_hits_str = [line.split('\t')[-2] for line in block if line]
                rt_hits_int = list(map(int, rt_hits_str))
                hits = len(rt_hits_int)
                rt_hits_mean = sum(rt_hits_int) / hits
                corrected_decimal = rt_hits_mean / 10
                full_rt_data[b, s[0], 1] += hits
                full_rt_data[b, s[0], 0] += corrected_decimal
    return full_rt_data

def logs_to_hitrate(log_dir):
    """Arrange behavioral data in a log file directory as a NumPy array."""
    full_data = np.zeros((4, 32, 5))
    for s in enumerate(os.listdir(log_dir)):
        if s[1] == 'desktop.ini':
            pass
        else:
            full_data[:, s[0], 4] = s[1][0:3]

            data = open(log_dir+'/'+s[1])
            data_lines = [line for line in data]
            test_lines = []
            for i in range(0, len(data_lines)):
                if 'test' in data_lines[i] and data_lines[i][0:7] != 'Picture':
                    test_lines.append(data_lines[i])
            test_lines_proper = test_lines[4:len(test_lines)]

            test_blocks = [test_lines_proper[i:i + 48] for i in range(0, len(test_lines_proper), 48)]
            for b in range(0, len(test_blocks)):
                for i in range(0, len(test_blocks[b])):
                    if 'hit' in test_blocks[b][i]:
                        full_data[b, s[0], 0] += 1    # hits
                    elif 'incorrect' in test_blocks[b][i]:
                        full_data[b, s[0], 1] += 1    # incorrects
                    else:
                        full_data[b, s[0], 2] += 1    # others
                full_data[b, s[0], 3] += full_data[b, s[0], 0] / full_data[b, s[0], 0:3].sum() * 100
                
    return full_data

def meg_sensors(info_data_dir):
    """Return MEG sensor info from a dummy file directory."""
    for path, dirs, files in os.walk(info_data_dir):
        for file in files:
            info_data = mne.io.read_raw_fif(
                path+'/'+file,
                preload=True,
                verbose=True
                )
    info = info_data.info
    meg_indices = mne.pick_types(
        info,
        meg=True
        )
    meg_info = mne.pick_info(
        info,
        meg_indices
        )
    return meg_info

#Remember to change for your own use
info_data_dir = 'C:/Users/eerou/Desktop/analyysi/data/meta'
meg_source_dir = 'C:/Users/eerou/Desktop/analyysi/data/neural'
perf_source_dir = 'C:/Users/eerou/Desktop/analyysi/data/behavioral' 
data_point_dir ='C:/Users/eerou/Desktop/analyysi/data/data_points'

full_rt_data = logs_to_rts(perf_source_dir)

data_points = []
data_points.append(['ID', 'N400 Mean Difference', 'Mean Reaction Time'])
sensors = meg_sensors(info_data_dir)
ch_blocks = sensors['ch_names'] * 4
for s in enumerate(os.listdir(meg_source_dir)):
    if s[1] == 'desktop.ini':
        pass
    else:
        meg_no_chs = np.loadtxt(
                meg_source_dir+'/'+s[1],
                delimiter=','
                )
        meg_data = [val for ch, val in zip(ch_blocks, meg_no_chs) if ch == 'MEG2542']
        rt_data = full_rt_data[0:4, s[0], 0]
        for dp in zip(meg_data, rt_data):
            data_point = []
            data_point.append(s[1][9:12])
            data_point.append(dp[0])
            data_point.append(dp[1])
            data_points.append(data_point)

df = pd.DataFrame(data_points)
df.to_csv(data_point_dir+'/'+'data_points.csv', 
          index=False, 
          header=False
         )

