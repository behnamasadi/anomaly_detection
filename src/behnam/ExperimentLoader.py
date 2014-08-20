'''
Created on Oct 20, 2011

@author: behnam
'''
import csv
import sys

f=open('/home/behnam/workspace/anomaly/src/dfki-experiment/20110818_Ramp_walking/0/1_0Deg_pattern1/telemetry.log')
#Number of Record X Number of Dimensions
Leg1=[]
Leg1Records=[]
try:
    reader = csv.DictReader(f)
    for row in reader:
        Leg1.append(row[" ACTUAL_JOINT_CURRENT_0"]) 
        Leg1.append(row[" ACTUAL_JOINT_CURRENT_1"])
        Leg1.append(row[" ACTUAL_JOINT_CURRENT_2"])
        Leg1.append(row[" ACTUAL_JOINT_CURRENT_3"])
        Leg1Records.append(Leg1)
        Leg1=[]
finally:
    f.close()
    
#print len(Leg1Records) 
print Leg1Records[0]
print Leg1Records[0][0] 
print Leg1Records[0][1]
print Leg1Records[0][2]
print Leg1Records[0][3]

