'''
Created on Oct 19, 2011

@author: behnam

This is the test module for rimres_telemetry_log_plot_test
In this file we have read data from one of our experiments and 
plot the Probability density function and also plot VS time 
'''
from rimres_telemetry_log_plot import *

PlotDensityFunctionForTelemetry_log(PathToDatabase='/home/behnam/workspace/anomaly/src/dfki-experiment/20110818_Ramp_walking/0/1_0Deg_pattern1/'
                      ,HistogramOrKDEPDF='Histogram',NumberOfBins=10000,NumberOfRecordsToBeSelected=-1)


#PlotTelemetry_log(PathToDatabase='/home/behnam/workspace/anomaly/src/dfki-experiment/20110818_Ramp_walking/0/1_0Deg_pattern1/'
#                      ,NumberOfRecordsToBeSelected=-1)