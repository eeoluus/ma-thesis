#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import mne

#Remember to rename for your own use
source_dir = 'C:/Users/eerou/Desktop/analyysi/data/neural/grand_averages/'
save_dir = 'C:/Users/eerou/Desktop/analyysi/test'

# This script first rearranges the data from a list of lists, each containing a single grand average, to another
# list of lists, each containing two grand averages per block. Second, it changes the condition labels to 
# something more informative than "Grand average". Third, it stores everything in a dictionary that can be accessed
# for plotting conditions in each block. An additional dictionary is created out of block-wise difference waves.

all_conds =     ['con', 'inc']*4
all_blocks =    ['block{}'.format(nr) for nr in range(1,5) for _ in range(2)]
all_evk_names = ['{}_{}'.format(b, c) for b, c in zip(all_blocks, all_conds)]
packed =        [mne.read_evokeds(source_dir+evk_name+'-ave.fif') for evk_name in all_evk_names]
unpacked =      [avg[0] for avg in packed]

def slicer(original, size):
    return [original[i:i+size] for i in range(0, len(original), size)]

block_evks =    slicer(unpacked, 2).copy()


block_evks[0][0].comment = 'Block 1 - Congruent'
block_evks[0][1].comment = 'Block 1 - Incongruent'
block_evks[1][0].comment = 'Block 2 - Congruent'
block_evks[1][1].comment = 'Block 2 - Incongruent'
block_evks[2][0].comment = 'Block 3 - Congruent'
block_evks[2][1].comment = 'Block 3 - Incongruent'
block_evks[3][0].comment = 'Block 4 - Congruent'
block_evks[3][1].comment = 'Block 4 - Incongruent'


gr_avg_keys = ['evks{}'.format(nr) for nr in range(1,5)]
gr_avgs = dict(zip(gr_avg_keys, block_evks))


gr_avg_diffs = [mne.combine_evoked(gr_avgs[x], weights=[1, -1]) for x in gr_avgs]
for nr in range(1,5):
    gr_avg_diffs[nr - 1].comment = 'Block {}: Congruent - Incongruent'.format(nr)
    gr_avg_diffs[nr - 1].nave = 32
gr_avg_diff_keys = ['diff{}'.format(nr) for nr in range(1,5)]
gr_avg_diffs = dict(zip(gr_avg_diff_keys, gr_avg_diffs))


#Plot the difference waves
plt.rcParams.update({'figure.dpi': 300})
for nr in range(1,5):
    gr_avg_diffs['diff'+str(nr)].nave = None
    fig = gr_avg_diffs['diff'+str(nr)].plot(
        picks='grad',
        show=False,
        ylim=dict(grad=[-22.5, 42.5]),
        spatial_colors=True,
        zorder='std',
        )
    ax = fig.get_axes()[0]
    ax.set_title(f'Block {nr}')
    for time in [0.3, 0.5]:
        ax.axvline(
            time,
            c='gray',
            lw=0.5
            )
    ax.axvspan(
        -0.2,
        0.3,
        color='gray',
        alpha=0.2
        )
    ax.axvspan(
        0.5,
        0.8,
        color='gray',
        alpha=0.2
        )
    ax.axvspan(
        -0.2,
        0.3,
        color='gray',
        alpha=0.2
        )
    ax.axvline(
        0,
        ls='dashed',
        lw=0.85,
        dashes=(7, 3.5),
        color='dimgray'
        )
    plt.savefig(save_dir+'/'+'difference_waves'+str(nr)+'.png')
    plt.show()

