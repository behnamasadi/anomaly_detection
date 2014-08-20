from c_index_kmeans import *

'''
This is the test module for c_index_kmeans, first we get data from the  GenerateData() function, then we find the optimal number of components 
aftre that step we  have optimal number of components==>IndexOfOptimalNumberOfComponents, we  initialize the GMM with our IndexOfOptimalNumberOfComponents+1
because the index start form zero
'''

#test data generated from some Gaussian distributions 
#Data=ReadFile()
Data=GenerateData()


#data coming form robot sensors 
#Data=ReadDataFromDB()[1]
#Data=Data.reshape(499,1)



NumberofIterationsForCindex=50
DistanceMethod='euclidean'
MaxNumberOfClusters=20

ListOfCindexes=[]
ListOfCenters=[]
MinimumOfCindexes=[]



CentersForCurrentCluster=[]
CindexForCurrentCluster=0

DistanceBetweenAllPairNodes = hcluster.pdist(Data, DistanceMethod)
DistanceBetweenAllPairNodesSorted= numpy.sort(DistanceBetweenAllPairNodes)

for NumberOfClusters in numpy.arange(1,MaxNumberOfClusters,1):
    CentersForCurrentCluster,CindexForCurrentCluster =ClusteringWithC_Index(Data, NumberOfClusters,NumberofIterationsForCindex,DistanceBetweenAllPairNodesSorted,DistanceMethod)
    ListOfCenters.append(CentersForCurrentCluster[:])
    ListOfCindexes.append(CindexForCurrentCluster)

IndexOfOptimalNumberOfComponents=numpy.argmin(ListOfCindexes)
Centers=ListOfCenters[IndexOfOptimalNumberOfComponents]

pyplot.figure()
pyplot.scatter(Data[:,0], Data[:,1]) 
pyplot.scatter( Centers[:,0], Centers[:,1],color='red')
pyplot.show()

g = mixture.GMM(n_states=IndexOfOptimalNumberOfComponents+1)
g._set_means(Centers)
g.fit(Data,init_params='wc')

print Centers.shape
print "Centers"
print numpy.sort(Centers,axis=0)
print "g.means"
print g.means
