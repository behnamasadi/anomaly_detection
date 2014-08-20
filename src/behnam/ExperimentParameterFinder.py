'''
Created on Oct 20, 2011

@author: behnam
'''
import csv
import sys
from sklearn import metrics
from sklearn import cluster
import numpy as numpy
import sklearn
import matplotlib.pyplot as plt
from  sklearn  import mixture
import matplotlib.pyplot as  pyplot


def GetParameterFromExperimnet(PathToExperimentFile):
    NumberOfRecordsToBeSelected=100
#    PathToExperimentFile='/home/behnam/workspace/anomaly/src/dfki-experiment/20110818_Ramp_walking/0/1_0Deg_pattern1/telemetry.log'
    f=open(PathToExperimentFile)
    #Number of Record X Number of Dimensions
    Leg1=[]
    Leg1Records=[]
    try:
        reader = csv.DictReader(f)
#        for row in min(len(reader),200):
        for row in reader:
            if reader.line_num>NumberOfRecordsToBeSelected:
                break
            else:    
                Leg1.append(int( row[" ACTUAL_JOINT_CURRENT_0"])) 
                Leg1.append(int( row[" ACTUAL_JOINT_CURRENT_1"]))
#                Leg1.append(int(row[" ACTUAL_JOINT_CURRENT_2"]))
#                Leg1.append(int( row[" ACTUAL_JOINT_CURRENT_3"]))
                Leg1Records.append(Leg1)
                Leg1=[]
    finally:
        f.close()
        
    #obs = numpy.concatenate( (numpy.random.randn(100, 2) , 20 + numpy.random.randn(300, 2) , -15+numpy.random.randn(200, 2)))
    
    obs=numpy.array(Leg1Records) 
    silhouette_score_values=list()
    NumberOfClusters=range(2,20)
    
    for i in NumberOfClusters:
        classifier=cluster.KMeans(k=i,init='k-means++', n_init=10, max_iter=300, tol=0.0001, verbose=0, random_state=None, copy_x=True)
        classifier.fit(obs)
        labels= classifier.predict(obs)
#        print "Number Of Clusters:"
#        print i
#        print "Silhouette score value"
#        print sklearn.metrics.silhouette_score(obs,labels ,metric='euclidean', sample_size=None, random_state=None)
        silhouette_score_values.append(sklearn.metrics.silhouette_score(obs,labels ,metric='euclidean', sample_size=None, random_state=None))
    
     
    plt.plot(NumberOfClusters, silhouette_score_values)
    plt.title("Silhouette score values vs NumberOfClusters ")
#    plt.show()
    
    Optimal_NumberOf_Components=NumberOfClusters[silhouette_score_values.index(max(silhouette_score_values))]
    print "Optimal Number Of Components is:"
    print Optimal_NumberOf_Components
      
    
    g = mixture.GMM(n_components=Optimal_NumberOf_Components)
#    g = mixture.GMM(n_components=10)
    g.fit(obs)
    
#    print "means:"
#    print g.means
#    
#    print "weights:"
#    print g.weights
#    
#    print "covars:"
#    print g.covars
    
    return g.means, g.weights,g.covars




  



