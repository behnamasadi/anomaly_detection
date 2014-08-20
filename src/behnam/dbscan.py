'''
Created on Jun 14, 2011

@author: behnam

DBSCAN (Density-Based Spatial Clustering of Applications with Noise) is a data clustering algorithm
It is a density-based clustering algorithm because it finds a number of clusters starting from the 
estimated density distribution of corresponding nodes.

DBSCAN requires two parameters: epsilon (eps) and the minimum number of points required to form a cluster (minPts).
It starts with an arbitrary starting point that has not been visited. This point's epsilon-neighborhood is 
retrieved, and if it contains sufficiently many points, a cluster is started. Otherwise, the point is labeled as
noise.
Note that this point might later be found in a sufficiently sized epsilon-environment of a different point and
hence be made part of a cluster.
If a point is found to be part of a cluster, its epsilon-neighborhood is also part of that cluster.
Hence, all points that are found within the epsilon-neighborhood are added, as is their own epsilon-neighborhood.
This process continues until the cluster is completely found. Then, a new unvisited point is retrieved and processed, leading to the discovery of a further cluster or noise.


#this is the pseudo code of dbscan which has been implemented:  
#DBSCAN(D, eps, MinPts)
#   C = 0
#   for each unvisited point P in dataset D
#      mark P as visited
#      N = getNeighbors (P, eps)
#      if sizeof(N) < MinPts
#         mark P as NOISE
#      else
#         C = next cluster
#         expandCluster(P, N, C, eps, MinPts)

#expandCluster(P, N, C, eps, MinPts)
#   add P to cluster C
#   for each point P' in N 
#      if P' is not visited
#         mark P' as visited
#         N' = getNeighbors(P', eps)
#         if sizeof(N') >= MinPts
#            N = N joined with N'
#      if P' is not yet member of any cluster
#         add P' to cluster C
'''
import numpy as numpy
import hcluster as hcluster 



def set2List(NumpyArray):
    list = []
    for item in NumpyArray:
        list.append(item.tolist())
    return list



def DBSCAN(Dataset, Epsilon,MinumumPoints,DistanceMethod = 'euclidean'):
#    Dataset is a mxn matrix, m is number of item and n is the dimension of data
    m,n=Dataset.shape
    Visited=numpy.zeros(m,'int')
    Type=numpy.zeros(m)
#   -1 noise, outlier
#    0 border
#    1 core
    ClustersList=[]
    Cluster=[]
    PointClusterNumber=numpy.zeros(m)
    PointClusterNumberIndex=1
    PointNeighbors=[]
    DistanceMatrix = hcluster.squareform(hcluster.pdist(Dataset, DistanceMethod))
    for i in xrange(m):
        if Visited[i]==0:
            Visited[i]=1
            PointNeighbors=numpy.where(DistanceMatrix[i]<Epsilon)[0]
            if len(PointNeighbors)<MinumumPoints:
                Type[i]=-1
            else:
                for k in xrange(len(Cluster)):
                    Cluster.pop()
                Cluster.append(i)
                PointClusterNumber[i]=PointClusterNumberIndex
                
                
                PointNeighbors=set2List(PointNeighbors)    
                ExpandClsuter(Dataset[i], PointNeighbors,Cluster,MinumumPoints,Epsilon,Visited,DistanceMatrix,PointClusterNumber,PointClusterNumberIndex  )
                Cluster.append(PointNeighbors[:])
                ClustersList.append(Cluster[:])
                PointClusterNumberIndex=PointClusterNumberIndex+1
                 
                    
    return PointClusterNumber 



def ExpandClsuter(PointToExapnd, PointNeighbors,Cluster,MinumumPoints,Epsilon,Visited,DistanceMatrix,PointClusterNumber,PointClusterNumberIndex  ):
    Neighbors=[]

    for i in PointNeighbors:
        if Visited[i]==0:
            Visited[i]=1
            Neighbors=numpy.where(DistanceMatrix[i]<Epsilon)[0]
            if len(Neighbors)>=MinumumPoints:
#                Neighbors merge with PointNeighbors
                for j in Neighbors:
                    try:
                        PointNeighbors.index(j)
                    except ValueError:
                        PointNeighbors.append(j)
                    
        if PointClusterNumber[i]==0:
            Cluster.append(i)
            PointClusterNumber[i]=PointClusterNumberIndex
    return