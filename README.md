# ma-thesis

The R script for replicating the statistics will be added in the near future.

Instructions for replicating the analysis. Behavioral data is read from Presentation log files (Neurobehavioral Systems), whereas the MEG data is assumed to be from the Elekta Neuromag TRIUX system (which uses the .fif extension).

Split preprocessed MEG data files with splitter.py
Calculate grand averages from split files using grand_averages.py
Plot grand averages with ga_plots.py
Calculate condition differences from split files using condition_differences.py
Plot t-heatmaps from condition differences using permutation_hmaps.py

Form data points on the basis of reaction times and condition differences with data_points.py
Plot reaction times and percentage of correct responses using hitrate_rt_plots.py
