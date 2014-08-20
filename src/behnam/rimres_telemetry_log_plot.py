''' 
This Module will plot the sensory data coming from scorpion, for each leg.
scorpion has six leg and 4 sensor for each one, so 6x4=24.
The function PlotDensityFunctionForTelemetry_log reads the data from a given sqlite data base and then in will draw the histogram or kdepdf(Kernel density estimation of probability distribution function)
  The Function PlotTelemetry_log() reads the data from a given sqlite data base and then in will plot them vs Time
'''
import numpy as numpy
from matplotlib import pyplot
import sqlite3
from scipy import stats
import csv
import sys



def PlotDensityFunctionForTelemetry_log(PathToDatabase='/home/behnam/workspace/anomaly/src/dfki-experiment/20110818_Ramp_walking/0/1_0Deg_pattern1/'
                      ,HistogramOrKDEPDF='Histogram',NumberOfBins=200,NumberOfRecordsToBeSelected=-1):
    Fields='''ACTUAL_JOINT_CURRENT_0,
    ACTUAL_JOINT_CURRENT_1,
    ACTUAL_JOINT_CURRENT_2,
    ACTUAL_JOINT_CURRENT_3,
    ACTUAL_JOINT_CURRENT_4,
    ACTUAL_JOINT_CURRENT_5,
    ACTUAL_JOINT_CURRENT_6,
    ACTUAL_JOINT_CURRENT_7,
    ACTUAL_JOINT_CURRENT_8,
    ACTUAL_JOINT_CURRENT_9,
    ACTUAL_JOINT_CURRENT_10,
    ACTUAL_JOINT_CURRENT_11,
    ACTUAL_JOINT_CURRENT_12,
    ACTUAL_JOINT_CURRENT_13,
    ACTUAL_JOINT_CURRENT_14,
    ACTUAL_JOINT_CURRENT_15,
    ACTUAL_JOINT_CURRENT_16,
    ACTUAL_JOINT_CURRENT_17,
    ACTUAL_JOINT_CURRENT_18,
    ACTUAL_JOINT_CURRENT_19,
    ACTUAL_JOINT_CURRENT_20,
    ACTUAL_JOINT_CURRENT_21,
    ACTUAL_JOINT_CURRENT_22,
    ACTUAL_JOINT_CURRENT_23,
    ACTUAL_JOINT_CURRENT_24'''
    
    
#    PathToDatabase='/home/behnam/workspace/anomaly/src/dfki-experiment/20110818_Ramp_walking/0/1_0Deg_pattern1/'
    PathToSave=PathToDatabase
    
    #The data that comes from sensors are between -20 and 20
    Range=[-5000,5000]
#    HistogramOrKDEPDF='Histogram'
    kdepdf=[]
    ListFields = [s.strip() for s in Fields.split(',')] 
#    NumberOfBins=200
    
#    NumberOfRecordsToBeSelected=500
    
#    TableName='telemetry_log'
#    connection = sqlite3.connect(PathToDatabase+ 'telemetry.log.csv.db')
#    cursor = connection.cursor()
#    SelectQuery='SELECT '+Fields+' FROM '+TableName +' limit ' + str(NumberOfRecordsToBeSelected)
    ind = numpy.linspace(-5000,5000,10001)
    X = [[] for j in range(0,24)]
    


    f=open('/home/behnam/workspace/anomaly/src/dfki-experiment/20110818_Ramp_walking/0/1_0Deg_pattern1/telemetry.log.csv')
    try:
        reader = csv.DictReader(f)
        for row in reader:
            for i in range(0,24):
                X[i]=str.strip(row[' ACTUAL_JOINT_CURRENT_'+str(i)])
#            print row[" ACTUAL_JOINT_CURRENT_1"]
    finally:
        f.close()
    
    
    
    
#    cursor.execute(SelectQuery)
#    for row in cursor:
#        if row[0]==' ':
#            pass
#        else :
#            for i in range(0,24):
#                X[i].append(float(row[i].strip()))
    
    for i in range(0,24,4):
        pyplot.figure()
        for j in range(1,5):
#           subplot(numRows, numCols, plotNum)
            pyplot.subplot(4,1,j)
            if HistogramOrKDEPDF=='Histogram':
                pyplot.hist(X[i+j-1], NumberOfBins, range=Range)
            else:
                gkde=stats.gaussian_kde(X[i+j-1])
                kdepdf = gkde.evaluate(ind)
                pyplot.plot(ind, kdepdf, color="g")
        pyplot.savefig(PathToSave+'/ACTUAL_JOINT_CURRENT_x_y_hist_kdepdf/ACTUAL_JOINT_CURRENT_'+str(i)+'_'+str(i+3)+'_'+HistogramOrKDEPDF+'.png')
    
    #pyplot.show()
#    cursor.close()
#    connection.close()
    print "job done successfully, The results are in "+ PathToSave+'/ACTUAL_JOINT_CURRENT_x_y_hist_kdepdf/ACTUAL_JOINT_CURRENT_'    
    return


def PlotTelemetry_log(PathToDatabase='/home/behnam/workspace/anomaly/src/dfki-experiment/20110818_Ramp_walking/0/1_0Deg_pattern1/'
                      ,NumberOfRecordsToBeSelected=-1):
    Fields='''ACTUAL_JOINT_CURRENT_0,
    ACTUAL_JOINT_CURRENT_1,
    ACTUAL_JOINT_CURRENT_2,
    ACTUAL_JOINT_CURRENT_3,
    ACTUAL_JOINT_CURRENT_4,
    ACTUAL_JOINT_CURRENT_5,
    ACTUAL_JOINT_CURRENT_6,
    ACTUAL_JOINT_CURRENT_7,
    ACTUAL_JOINT_CURRENT_8,
    ACTUAL_JOINT_CURRENT_9,
    ACTUAL_JOINT_CURRENT_10,
    ACTUAL_JOINT_CURRENT_11,
    ACTUAL_JOINT_CURRENT_12,
    ACTUAL_JOINT_CURRENT_13,
    ACTUAL_JOINT_CURRENT_14,
    ACTUAL_JOINT_CURRENT_15,
    ACTUAL_JOINT_CURRENT_16,
    ACTUAL_JOINT_CURRENT_17,
    ACTUAL_JOINT_CURRENT_18,
    ACTUAL_JOINT_CURRENT_19,
    ACTUAL_JOINT_CURRENT_20,
    ACTUAL_JOINT_CURRENT_21,
    ACTUAL_JOINT_CURRENT_22,
    ACTUAL_JOINT_CURRENT_23,
    ACTUAL_JOINT_CURRENT_24'''
    TableName='telemetry_log'
    connection = sqlite3.connect(PathToDatabase+ 'telemetry.log.csv.db')
    cursor = connection.cursor()
    SelectQuery='SELECT '+Fields+' FROM '+TableName +' limit ' + str(NumberOfRecordsToBeSelected)
    PathToSave=PathToDatabase
    
    X = [[] for j in range(0,24)]
    
    cursor.execute(SelectQuery)
    for row in cursor:
        if row[0]==' ':
            pass
        else :
            for i in range(0,24):
                X[i].append(float(row[i].strip()))
    
    
    for i in range(0,24,4):
        pyplot.figure()
        for j in range(1,5):
            pyplot.subplot(4,1,j)
#            subplot(numRows, numCols, plotNum)
#            gkde=stats.gaussian_kde(X[i+j-1])
#            kdepdf = gkde.evaluate(ind)
            pyplot.plot(X[i+j-1], color="g")
#        pyplot.savefig(PathToSave+'/ACTUAL_JOINT_CURRENT_x_y_hist/ACTUAL_JOINT_CURRENT_'+str(i)+'_'+str(i+3)+'_'+HistogramOrKDEPDF+'.svg')
        pyplot.savefig(PathToSave+'/ACTUAL_JOINT_CURRENT_x_y_plot/ACTUAL_JOINT_CURRENT_'+str(i)+'_'+str(i+3)+'_'+'.svg')
    print "job done successfully, The results are in "+ PathToSave+'/ACTUAL_JOINT_CURRENT_x_y_plot/ACTUAL_JOINT_CURRENT_'
    return 

#select max(ACTUAL_JOINT_CURRENT_7) from telemetry_log

#select max(ACTUAL_JOINT_CURRENT_15) from telemetry_log==>2748