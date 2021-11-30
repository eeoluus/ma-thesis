#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import numpy as np
import scipy
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import mne
from mne.stats import permutation_t_test

#Remember to rename these for your own use
metadata_dir = 'C:/Users/eerou/Desktop/analyysi/data/meta'
source_dir = 'C:/Users/eerou/Desktop/analyysi/data/neural'
save_dir = 'C:/Users/eerou/Desktop/analyysi/test'

#For getting information about MEG sensor coordinates to be transformed into RGB values
for path, dirs, files in os.walk(metadata_dir):
    for file in files:
        block = mne.io.read_raw_fif(
            path+'/'+file,
            preload=True,
            verbose=True
            )
info = block.info
meg_indices = mne.pick_types(
    info,
    meg=True
    )
meg_info = mne.pick_info(
    info,
    meg_indices
    )
ch_coordinates = np.array([ch['loc'][:3] for ch in meg_info['chs']])
x, y, z = ch_coordinates.T
rgb = np.array([x, y, z]).T
rgb -= rgb.min(0)
rgb /= np.maximum(
    rgb.max(0),
    1e-16
    )

#Reads the data from .csv files and computes the permutation statistics
data_list = []
for path, dirs, files in os.walk(source_dir):
    for file in files:
        data = np.loadtxt(
            path+'/'+file,
            delimiter=','
            )
        data_list.append(data)
data_array = np.array(data_list)

#For TFCE, the adjacency matrix must be defined before this
t_obs, p_values, tmax_distr = mne.stats.permutation_t_test(
    data_array,
    n_permutations=100000,
    tail=0
    )
block_t_obs = np.split(
    t_obs,
    4
    )
block_p_values = np.split(
    p_values,
    4
    )
hist = np.histogram(
    tmax_distr,
    bins='auto'
    )
hist_dist = scipy.stats.rv_histogram(hist)
critical_t = hist_dist.ppf(0.95)

#Determines where the greatest t-statistic was obtained
high_t = max(
    t_obs.min(), 
    t_obs.max(), 
    key=abs
    )
index = np.where(block_t_obs == high_t)
block = index[0][0]
sensor = index[1][0]
high_t_sensor = meg_info['ch_names'][sensor]
print(f'The greatest t-statistic is found at the sensor {high_t_sensor} during block {block+1} with a value of {high_t}.')

#Determines where the smallest p-value was obtained
low_p = min(p_values)
index = np.where(block_p_values == low_p)
block = index[0][0]
sensor = index[1][0]
low_p_sensor = meg_info['ch_names'][sensor]
print(f'The lowest p-value is found at the sensor {high_t_sensor} during block {block+1} with a value of {low_p}.')

#Renames the sensor labels for readable color coding
new_names = ['___']*306
blocks = [str(nr) for nr in range(1, 5)]
t_frame = pd.DataFrame(
        data=block_t_obs,
        columns=pd.Index(
            new_names,
            name='Channel'
            ),
        index=pd.Index(
            blocks,
            name='Block'
            )
        )

#Plots a heatmap of t-statistics with color-coded sensors
plt.rcParams.update({'figure.dpi': 120})
fig, ax = plt.subplots(
    1, 
    1, 
    figsize=(12, 8)
    )
sns.heatmap(
    data=t_frame,
    vmin=-7.58527515,
    vmax=7.58527515,
    cmap='RdBu_r',
    cbar_kws=dict(label='T-values'),
    xticklabels=True
    )
for nr in range(0, 306):
    ax.get_xticklabels()[nr].set_color(rgb[nr])
ax.tick_params(
    axis='x', 
    labelsize=27.5
    )
dx = -11.80/72. 
dy = 0/72. 
offset = matplotlib.transforms.ScaledTranslation(
    dx,
    dy,
    fig.dpi_scale_trans
    )
for label in ax.xaxis.get_majorticklabels():
    label.set_transform(label.get_transform() + offset)
ax.set_title(
    'T-heatmap',
    fontsize=16,
    fontweight='bold',
    y=1.1
    )    
cbar = fig.get_axes()[1]
cbar.axhline(
    critical_t,
    ls='dotted',
    lw=0.9,
    dashes=(1,2),
    color='black',
    zorder=500
    )
cbar.axhline(
    -critical_t,
    ls='dotted',
    lw=0.9,
    dashes=(1,2),
    color='black',
    zorder=500
    )
cbar.axhline(
    max(t_obs),
    lw=0.50,
    color='black',
    zorder=500
    )
cbar.axhline(
    min(t_obs),
    lw=0.50,
    color='black',
    zorder=500
    )
plt.tick_params(bottom=False)
plt.savefig(save_dir+'/'+'t-heatmap.png')


# In[ ]:




