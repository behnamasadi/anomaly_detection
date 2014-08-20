# coding: utf-8
'''
Created on Oct 19, 2011

@author: behnam

This is the test module for comparing two pdf and finding the distance between them.
First we have generate two data set, namely obs1, obs2.
obs1 and obs2 are mixture of Gaussians with different number of components, different mean.
Then We have approximated the weight, means and covariance matrix for obs1 and obs2 with EM algorithm.
In the Last step we have found the distance between them.  
'''
import numpy as numpy
#from scikits.learn import mixture
from sklearn import mixture
import matplotlib.pyplot as pyplot
from PDFComparison import *

obs1 = numpy.concatenate((numpy.random.randn(100, 2) , 10 + numpy.random.randn(300, 2) , -5+numpy.random.randn(200, 2)))
g1 = mixture.GMM(n_components=3,cvtype='diag')
g1.fit(obs1)

#print "First Observation"
#print "means"    
#print g1.means
#print "weights"
#print g1.weights

obs2 = numpy.concatenate(( numpy.random.randn(400, 2) ,
                           numpy.random.randn(100, 2)+5 ,
                           numpy.random.randn(300,2)+8,
                           numpy.random.randn(300,2)-12,
                           numpy.random.randn(200,2)+18  ) 
                         )
g2 = mixture.GMM(n_components=5,cvtype='diag')
g2.fit(obs2)

#print "______________________________________________________________________________________________________________________________"
#print "Second Observation"
#print "means"    
#print g2.means
#print "weights"
#print g2.weights

pyplot.scatter(obs1[:,0],obs1[:,1])
pyplot.scatter(g1.means[:,0],g1.means[:,1],color='red')
pyplot.show()

pyplot.scatter(obs2[:,0],obs2[:,1])
pyplot.scatter(g2.means[:,0],g2.means[:,1],color='red')

pyplot.show()

#First GMM:
Means=g1.means
Weights=g1.weights
CovarianceMatrices=g1.covars 

#Second GMM:
Means_Prime=g2.means
Weights_Prime=g2.weights
CovarianceMatrices_Prime=g2.covars


print "Means"
print Means

print "Weights"
print Weights

print "CovarianceMatrices" 
print CovarianceMatrices



print "Means_Prime"
print Means_Prime

print "Weights_Prime"
print Weights_Prime

print "CovarianceMatrices_Prime" 
print CovarianceMatrices_Prime


print "TotalDistance"
print TotalDistance(Weights, Means, CovarianceMatrices, Weights_Prime, Means_Prime, CovarianceMatrices_Prime)
#print TotalDistance(Weights, Means, CovarianceMatrices, Weights, Means, CovarianceMatrices)
