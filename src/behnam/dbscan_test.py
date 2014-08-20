'''
Created on Oct 19, 2011

@author: behnam
This is the test module for dbscan 
Here the data point are blue, noise are red and black dots are the point that DBSCAN has detected as noise.
'''
from dbscan import * 
import pylab as pylab
import scipy as scipy
import numpy as numpy

x1 = scipy.rand(30,2)*2
x2 =scipy.rand(40,2)*2+4
x3x = scipy.rand(30,1)+8
x3y=scipy.rand(30,1)



x3=numpy.column_stack((x3x,x3y))
xy= numpy.concatenate((x1,x2))

noise=scipy.rand(50,2)*10

Data=numpy.concatenate((x1,x2,x3,noise))

pylab.scatter(x1[:,0],x1[:,1], alpha =  0.5)
pylab.scatter(x2[:,0],x2[:,1], alpha =  0.5)
pylab.scatter(x3[:,0],x3[:,1], alpha =  0.5)
pylab.scatter(noise[:,0],noise[:,1],color='red' ,alpha =  0.5)

result =DBSCAN(Data,1,20)
print result
print "Data"
print Data.shape
print Data
for i in xrange(len(result)):
    if result[i]==0:
        pylab.scatter(Data[i][0],Data[i][1],color='black' ,alpha =  1)
        

pylab.show()