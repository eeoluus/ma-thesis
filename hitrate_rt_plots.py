#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import numpy as np
import matplotlib.pyplot as plt

# This script creates a behavioral data array of shape b blocks (rows) x s subjects (columns) x 4 data values. The values are
# hits, incorrect answers, other outcomes and subject IDs. After constructing an array of zeros, the data is (1) loaded from log
# files, which are truncated to exclude duplicates, practise and other than test data. It is then (2) split into blocks and
# analyzed block-wise, with results added to the array of zeros.

def logs_to_performance(log_dir):

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

            # Pitää jotenkin varmistaa, että trialien määrä todellakin on 192, tai sitten implementoida jotenkin muuten

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

            # Pitää jotenkin varmistaa, että trialien määrä todellakin on 192, tai sitten implementoida jotenkin muuten

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

#Remember to rename for your own use
info_data_dir = 'C:/Users/eerou/Desktop/analyysi/data/meta'
meg_source_dir = 'C:/Users/eerou/Desktop/analyysi/data/neural'
perf_source_dir = 'C:/Users/eerou/Desktop/analyysi/data/behavioral' 
save_dir = 'C:/Users/eerou/Desktop/analyysi/test'

full_data0 = logs_to_performance(perf_source_dir)
full_data1 = logs_to_rts(perf_source_dir)
plt.rcParams.update({'figure.dpi': 300})

fig, ax = plt.subplots()
for s in range(0, len(full_data0[0, :, 4])):
    scores_per_block = full_data0[:, s, 3]
    ax.plot(
        [1, 2, 3, 4], 
        scores_per_block
        )
ax.set_title('Learning curves')
ax.set_xticks([1, 2, 3, 4])
ax.set_ylabel('Percent correct')
ax.set_xlabel('Block')
plt.savefig(save_dir+'/'+'hitrate_plot.png')
plt.show()

fig, ax = plt.subplots()
for s in range(0, len(full_data1[0, :, 2])):
    scores_per_block = full_data1[:, s, 0]
    ax.plot(
        [1, 2, 3, 4], 
        scores_per_block
        )
ax.set_title('Learning curves')
ax.set_xticks([1, 2, 3, 4])
ax.set_ylabel('Reaction times (ms)')
ax.set_xlabel('Block')
plt.savefig(save_dir+'/'+'rt_plot.png')
plt.show()

