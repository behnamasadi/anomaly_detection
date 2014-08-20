#http://scikit-learn.org/stable/modules/generated/sklearn.metrics.silhouette_score.html
#print sklearn.__version__


from sklearn import metrics
from sklearn import cluster
import numpy as numpy
import sklearn
import matplotlib.pyplot as plt
from  sklearn  import mixture
import matplotlib.pyplot as  pyplot

obs = numpy.concatenate( (numpy.random.randn(100, 2) , 20 + numpy.random.randn(300, 2) , -15+numpy.random.randn(200, 2)))
silhouette_score_values=list()

NumberOfClusters=range(2,30)

for i in NumberOfClusters:
    
    classifier=cluster.KMeans(k=i,init='k-means++', n_init=10, max_iter=300, tol=0.0001, verbose=0, random_state=None, copy_x=True)
    classifier.fit(obs)
    labels= classifier.predict(obs)
    print "Number Of Clusters:"
    print i
    print "Silhouette score value"
    print sklearn.metrics.silhouette_score(obs,labels ,metric='euclidean', sample_size=None, random_state=None)
    silhouette_score_values.append(sklearn.metrics.silhouette_score(obs,labels ,metric='euclidean', sample_size=None, random_state=None))





plt.plot(NumberOfClusters, silhouette_score_values)
plt.title("Silhouette score values vs NumberOfClusters ")
plt.show()

Optimal_NumberOf_Components=NumberOfClusters[silhouette_score_values.index(max(silhouette_score_values))]
print "Optimal Number Of Components is:"
print Optimal_NumberOf_Components
  

g = mixture.GMM(n_components=Optimal_NumberOf_Components)
g.fit(obs)
pyplot.scatter(obs[:,0],obs[:,1])
pyplot.scatter(g.means[:,0],g.means[:,1],color='red')

pyplot.show()
  
