# coding: utf-8
import matplotlib.pyplot as pyplot
import numpy as numpy
from scikits.learn import cluster
import hcluster as hcluster 
import math as math
import sys
from scikits.learn import mixture
import sqlite3
from scipy.cluster.vq import vq, kmeans, whiten,kmeans2

'''
This module find the optimal number number of component for a given data.
In order to find the optimal number of components for, first we used k-means algorithm
with different number of clusters (starting from 1 to a fixed number), 

please read this documentation for more info about kmean algorithm
http://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.vq.kmeans.html#scipy.cluster.vq.kmeans
http://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.vq.kmeans2.html#scipy.cluster.vq.kmeans2


then we checked the cluster validity by deploying C-index algorithm and select the optimal number of
clusters with lowest C-index. This index  is defined as follows:

C=(S − Smin)/(Smax − Smin)
where S is the sum of distances over all pairs of patterns from the same cluster. Let l
be the number of those pairs. Then Smin is the sum of the l smallest distances if all
pairs of patterns are considered (i.e. if the patterns can belong to different clusters).
Similarly Smax is the sum of the l largest distance out of all pairs. Hence a small value
of C indicates a good clustering.


you can use:
 GenerateData() function which generate some test data or you can use 
 ReadFile() function which read data points form the cluster_dataset2d file or you can use 
 ReadDataFromDB() to read data from sqlite db 
'''

def ReadDataFromDB(AbsolutePathToDatbaseFile='/home/behnam/workspace/anomaly/src/simulation-data/Normal Walking_Log_Plot/-100/telemetry.log.csv.db',NumberOfRecordsToBeSelected=500):
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
    connection = sqlite3.connect(AbsolutePathToDatbaseFile)
    cursor = connection.cursor()
    SelectQuery='SELECT '+Fields+' FROM '+TableName +' limit ' + str(NumberOfRecordsToBeSelected)
    
#    We have six legs, and each leg has 4 sensors, plus one sensor for all, so we would have 25 column in our select query, we would put their data
#    in X  
    X = [[] for j in range(0,24)]
    cursor.execute(SelectQuery)
    for row in cursor:
        if row[0]==' ':
#            in the case that nothing is in that column we would just escape            
            pass
        else :
            for i in range(0,24):
                X[i].append(float(row[i].strip()))
    return numpy.asarray(X)


def Combination(n,r):
    if n<r: 
        return 0 
    else :
        return math.factorial(n)/( math.factorial(n-r) * math.factorial(r ))


def GenerateData():
    x1=numpy.random.randn(50,2)
    x2x=numpy.random.randn(80,1)+2
    x2y=numpy.random.randn(80,1)-2
    x2=numpy.column_stack((x2x,x2y))
    x3=numpy.random.randn(30,2)+8
    x4=numpy.random.randn(120,2)+12
    z=numpy.concatenate((x1,x2,x3,x4))
    return z


def ReadFile():
    f = open('cluster_dataset2d','r')
    z=[]
    for line in f:
        line=line.strip()
        x=line.split(' ')
        z.append(float(x[0]))
        z.append(float(x[1]))
    z=numpy.array(z)
    z=z.reshape(151,2)
    return z


def ShowDataWithOptimalCenters(Data,OptimalCenters):
    pyplot.scatter(Data[:,0],Data[:,1])
    pyplot.scatter(OptimalCenters[:,0],OptimalCenters[:,1],color='red')
    pyplot.show()
    return


def oldClusteringWithC_Index(Data,NumberOfClusters,NumberofIterationsForCindex,DistanceBetweenAllPairNodesSorted,DistanceMethod='euclidean'):
    NumberOfClusters=NumberOfClusters
    x=Data
    NumberofIterationsForCindex=NumberofIterationsForCindex
    NUmberOfNodesInTheClusters=0
    D=DistanceBetweenAllPairNodesSorted
    OptimalCenter=[]
    
    C=1
    Old_C=sys.maxint
    Scl=0
    N=0
    Smin=0
    Smax=0


    for NumberofIterations in xrange(NumberofIterationsForCindex):
        #init : {'k-means++', 'random', 'points','matrix'}
        #'k-means++' : selects initial cluster centers for k-mean clustering in a smart way to speed up convergence
        # http://scikit-learn.sourceforge.net/modules/generated/scikits.learn.cluster.KMeans.html#scikits.learn.cluster.KMeans
        classifier=cluster.KMeans(k=NumberOfClusters, init='random', n_init=10, max_iter=300, tol=0.0001, verbose=0, random_state=None, copy_x=True)
        y=classifier.fit(x)
        for i in xrange( NumberOfClusters ):
#            print 'NumberofIterations'
#            print NumberofIterations
#            print 'NumberOfClusters'
#            print NumberOfClusters
#            print 'classifier.cluster_centers_'
#            print classifier.cluster_centers_
            NUmberOfNodesInTheClusters=len(x[numpy.where(classifier.labels_==i)])
            Scl=Scl+numpy.sum( hcluster.pdist(x[numpy.where(classifier.labels_==i)], DistanceMethod))
            N=N+Combination(NUmberOfNodesInTheClusters, 2)
        Smin=numpy.sum( D[0:N:1])
        Smax=numpy.sum(D[len(D)-N::1])
        C=(Scl-Smin)/(Smax-Smin)
        Scl=0
        N=0
        Smin=0
        Smax=0
        if(C<Old_C):
            Old_C=C
            OptimalCenter=classifier.cluster_centers_[:]

    
    return OptimalCenter,Old_C


def ClusteringWithC_Index(Data,NumberOfClusters,NumberofIterationsForCindex,DistanceBetweenAllPairNodesSorted,DistanceMethod='euclidean'):
    NumberOfClusters=NumberOfClusters
    x=Data
    NumberofIterationsForCindex=NumberofIterationsForCindex
    NUmberOfNodesInTheClusters=0
    D=DistanceBetweenAllPairNodesSorted
    OptimalCenter=[]
    C=1
    Old_C=sys.maxint
    Scl=0
    N=0
    Smin=0
    Smax=0


    for NumberofIterations in xrange(NumberofIterationsForCindex):
        centroid,labels=Classifier=kmeans2(Data, NumberOfClusters, iter=500, thresh=1e-05, minit='random', missing='warn')
        for i in xrange( NumberOfClusters ):
            NUmberOfNodesInTheClusters=len(x[numpy.where(labels==i)])
            Scl=Scl+numpy.sum( hcluster.pdist(x[numpy.where(labels==i)], DistanceMethod))
            N=N+Combination(NUmberOfNodesInTheClusters, 2)
        Smin=numpy.sum( D[0:N:1])
        Smax=numpy.sum(D[len(D)-N::1])
        C=(Scl-Smin)/(Smax-Smin)
        Scl=0
        N=0
        Smin=0
        Smax=0
        if(C<Old_C):
            Old_C=C
            OptimalCenter=centroid[:]
    return OptimalCenter,Old_C




