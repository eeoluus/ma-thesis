# ma-thesis

Instructions for replicating the analysis. Behavioral data is read from Presentation log files (Neurobehavioral Systems), whereas the MEG data is assumed to be from an Elekta Neuromag TRIUX system (which uses the .fif extension). Please note that you have to **set up the input and output directories** for each step and change the scripts accordingly.


1. Split preprocessed MEG data files with splitter.py  
2. Calculate grand averages from split files using grand_averages.py  
3. Plot grand averages with ga_plots.py  
4. Calculate condition differences from split files using condition_differences.py  
5. Plot t-heatmaps from condition differences using permutation_hmaps.py  
6. Form data points on the basis of reaction times and condition differences with data_points.py  
7. Plot reaction times and percentage of correct responses using hitrate_rt_plots.py
8. Perform statistical analysis and plot the model and the data with statistics.r
9. Perform statistical analysis on reaction times by regressing on block number with statistics_behav.r
