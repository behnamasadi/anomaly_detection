'''
Created on Feb 13, 2012

@author: behnam
'''
from  ExperimentParameterFinder import *
from PDFComparison import *
import numpy as numpy



#Means=g1.means
#Weights=g1.weights
#CovarianceMatrices=g1.covars 

#Second GMM:
#Means_Prime=g2.means
#Weights_Prime=g2.weights
#CovarianceMatrices_Prime=g2.covars


PathToExperimentFile='/home/behnam/workspace/anomaly/src/dfki-experiment/20110818_Ramp_walking/0/1_0Deg_pattern3/telemetry.log'
Means, Weights,CovarianceMatrices=  GetParameterFromExperimnet(PathToExperimentFile)



print "Means"
print Means
print "Weights"
print Weights
print "CovarianceMatrices"
print CovarianceMatrices


PathToExperimentFile='/home/behnam/workspace/anomaly/src/dfki-experiment/20110818_Ramp_walking/0/1_0Deg_pattern1/telemetry.log'
Means_Prime,Weights_Prime, CovarianceMatrices_Prime=GetParameterFromExperimnet(PathToExperimentFile)


#for i in range(len(CovarianceMatrices)):
#    print numpy.linalg.inv(CovarianceMatrices[i])
#
#
#for i in range(len(CovarianceMatrices_Prime)):
#    print numpy.linalg.inv(CovarianceMatrices_Prime[i])



#print TotalDistance(Weights, Means, CovarianceMatrices, Weights_Prime, Means_Prime, CovarianceMatrices_Prime)


print "Weights_Prime"
print Weights_Prime
print  "Means_Prime"
print  Means_Prime  
print "CovarianceMatrices_Prime"
print CovarianceMatrices_Prime

