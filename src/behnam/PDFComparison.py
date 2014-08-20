# coding: utf-8
'''
Created on Sep 30, 2011

@author: behnam

This is PDFComparison function, which compare the distance between two GMM.
for more info about the implemented algorithm refer to :

G. Sfikas, C. Constantinopoulos, A. Likas, and N. Galatsanos. An analytic dis-
tance metric for gaussian mixture models with application in image retrieval. In
Wlodzislaw Duch, Janusz Kacprzyk, Erkki Oja, and Slawomir Zadrozny, edi-
tors, Artificial Neural Networks: Formal Models and Their Applications ICANN
2005, volume 3697 of Lecture Notes in Computer Science, pages 755–755.
Springer Berlin / Heidelberg, 2005. ISBN 978-3-540-28755-1. URL http://dx.doi.org/10.1007/11550907_132.


The latex code for the implemented formula is:



    \begin{equation} \label{Kullback_Liebler_divergence}
    D_{KL}(p||p^{\prime})=\int_{-\infty}^\infty p(x)\log\frac{p(x)}{p^{\prime}(x)}  \,\mathrm{d}x
    \end{equation}
    which could be used to calculate the distance between two arbitrary distribution including two Gaussians, but in our case we have a mixture of Gaussians for each distribution and therefore it is not possible to apply the equation. \citet{An_Analytic_Distance_Metric_for_Gaussian_Mixture_Models} have extended the Kullback Liebler divergence for GMM and proposed a distance metric using the values \(\mu ,\Sigma,\pi \) for each one of the two distributions in the following form:
    
    \begin{equation} \label{Kullback_Liebler_divergence}
    C2(p||p^{\prime})=-\log \large[ \frac{2\sum_{i,j}\pi_{i}\pi_{j}^{\prime} \sqrt{ \frac{|V_{ij}|}{e^{k_{ij}}|\sum_{i}| |\sum_{j}^{\prime}|} }  }
    %denominator
    {
    %left part
    \sum_{i,j}\pi_{i}\pi_{j} \sqrt{ \frac{|V_{ij}|}{e^{k_{ij}}|\sum_{i}| |\sum_{j}|} }+
    %right part
    \sum_{i,j}\pi_{i}^{\prime}\pi_{j}^{\prime} \sqrt{ \frac{|V_{ij}|}{e^{k_{ij}}|\sum_{i}^{\prime}| |\sum_{j}^{\prime}|} }
    } 
    \large]
    \end{equation}
    Where:
    \begin{equation}\label{Kullback_Liebler_divergence_Details1}
    V_{ij}=(\Sigma_{i}^{-1} +\Sigma_{j}^{-1})^{-1}
    \end{equation}
    and
    \begin{equation}\label{Kullback_Liebler_divergence_Details2}
    K_{ij}=\mu_{i}^{T}\Sigma_{i}^{-1}(\mu_{i}-\mu_{j}^{\prime})+\mu_{j}^{\prime T}\Sigma_{j}^{\prime -1}(\mu_{j}^{\prime}-\mu_{i})
    \end{equation}


'''
import numpy as numpy
#from scikits.learn import mixture
from sklearn import mixture
import matplotlib.pyplot as pyplot

#Begin Old Implementation

def VIJ_Determinant(I,J,CovarianceMatrix,CovarianceMatrix_Prime):
    Covariance_I_Inverse=numpy.linalg.inv(CovarianceMatrix)
    Covariance_Prime_J_Inverse=numpy.linalg.inv(CovarianceMatrix_Prime)
    return numpy.linalg.det(Covariance_I_Inverse+Covariance_Prime_J_Inverse)


def e_Power_KIJ(I,J,CovarianceMatrix,CovarianceMatrix_Prime,Means,Means_Prime):
    Covariance_I_Inverse=numpy.linalg.inv(CovarianceMatrix)
    Covariance_Prime_J_Inverse=numpy.linalg.inv(CovarianceMatrix_Prime)
   
    Mu_I=Means[I]
    Mu_Prime_J=Means_Prime[J]
    
    Mu_I.shape=Mu_I.shape[0],1
    Mu_Prime_J.shape=Mu_Prime_J.shape[0],1
    KIJ_LeftSide=numpy.dot( numpy.dot(Mu_I.transpose(),Covariance_I_Inverse),Mu_I-Mu_Prime_J)
    KIJ_RightSide=numpy.dot( numpy.dot(Mu_Prime_J.transpose(),Covariance_Prime_J_Inverse),Mu_Prime_J-Mu_I)
    KIJ=KIJ_RightSide+KIJ_LeftSide  
    return numpy.exp(KIJ)


def SigmaIterator(Covariance_I,Covariance_J,Means_I,Means_J,Pi_I,Pi_J,I,J):
    Covariance_I_Determinant=numpy.linalg.det(Covariance_I)
    Covariance_J_Determinant=numpy.linalg.det(Covariance_J)
    Second_Root=numpy.power(VIJ_Determinant(I,J,Covariance_I,Covariance_J)/(e_Power_KIJ(I,J,Covariance_I,Covariance_J,Means_I,Means_J)* Covariance_I_Determinant*Covariance_J_Determinant),0.5)
    return Pi_I*Pi_J*Second_Root


def Summation(Pis,Pis_Prime,Covariance,Covariance_Prime,Means_I,Means_J):
    Sum=0
    for I in range(len(Pis)):
#        print "I"
#        print I
        for J in  range(len(Pis_Prime)):
#            print "J"
#            print J
            Sum=Sum+SigmaIterator(Covariance[I],Covariance_Prime[J],Means_I,Means_J,Pis[I],Pis_Prime[J],I,J)            
    return Sum

#End of Old Implementation





#Begin New Implementation

def Numerator(Weights,Means,CovarianceMatrices,Weights_Prime,Means_Prime,CovarianceMatrices_Prime):
#    CovarianceMatrices and CovarianceMatrices_Prime are 3D Matrixes and have the below structure:
#    NumberOfComponents*NumberofDimensions*NumberofDimensions
#    in fact a list of N*N Arrays, which N is NumberofDimensions

#    Weights and Weights_Prime have the below structure:
#    NumberOfComponents*1

#    Means and Means_Prime have the below structure:
#    NumberOfComponents*NumberofDimensions
  
    Sum=0
    for i in range(len(CovarianceMatrices)):
        for j in range(len(CovarianceMatrices_Prime)):
            
            CovarianceMatrices_i_Inverse=numpy.linalg.inv(CovarianceMatrices[i])
            CovarianceMatrices_Prime_j_Inverse=numpy.linalg.inv( CovarianceMatrices_Prime[j])
            
            
            
            VIJ=numpy.linalg.inv( CovarianceMatrices_i_Inverse + CovarianceMatrices_Prime_j_Inverse)
            VIJ_Determinant=numpy.linalg.det(VIJ )
            
            Means_i_Transpose=numpy.transpose(Means[i])
            Means_Prime_j_Transpose=numpy.transpose(Means_Prime[j])
            
            KIJ=numpy.dot(   numpy.dot(Means_i_Transpose, CovarianceMatrices_i_Inverse  ) ,  Means[i]-Means_Prime[j]  )  + numpy.dot( numpy.dot(  Means_Prime_j_Transpose  ,  CovarianceMatrices_Prime_j_Inverse )      , Means_Prime[j]-Means[i]  )
            
            numerator=VIJ_Determinant
            denominator=numpy.exp(KIJ)*numpy.linalg.det(CovarianceMatrices[i])*numpy.linalg.det(CovarianceMatrices_Prime[j])
            Sum=Sum+Weights[i]*Weights_Prime[j]*numpy.sqrt(numerator/denominator) 
    return Sum;




def Denominator(Weights,Means,CovarianceMatrices):
    Sum=0
    for i in range(len(CovarianceMatrices)):
        print "i:"
        print i
        for j in range(len(CovarianceMatrices)):
            print "j:"
            print j
            Means_i_Transpose=numpy.transpose(Means[i])
            print "Means_i_Transpose"
            print Means_i_Transpose
            
            CovarianceMatrixs_i_Inverse=numpy.linalg.inv(CovarianceMatrices[i])
            print "CovarianceMatrixs_i_Inverse"
            print CovarianceMatrixs_i_Inverse
            
            Means_j_Transpose=numpy.transpose(Means[j])
            print "Means_j_Transpose"
            print Means_j_Transpose
            
            CovarianceMatrixs_j_Inverse=numpy.linalg.inv( CovarianceMatrices[j])
            print "CovarianceMatrixs_j_Inverse"
            print CovarianceMatrixs_j_Inverse
            
            VIJ=numpy.linalg.inv( CovarianceMatrixs_i_Inverse + CovarianceMatrixs_j_Inverse)
            print "VIJ"
            print VIJ
            
            VIJ_Determinant=numpy.linalg.det(VIJ )
            print "VIJ_Determinant"
            print VIJ_Determinant
            
            KIJ=numpy.dot(   numpy.dot(Means_i_Transpose, CovarianceMatrixs_i_Inverse  ) ,  Means[i]-Means[j]  )  + numpy.dot( numpy.dot(  Means_j_Transpose  ,  CovarianceMatrixs_j_Inverse )      , Means[j]-Means[i]  )
            print "KIJ"
            print KIJ
            
            numerator=VIJ_Determinant
            print "numerator"
            print numerator
            
            denominator=numpy.exp(KIJ)*numpy.linalg.det(CovarianceMatrices[i])*numpy.linalg.det(CovarianceMatrices[j])
            print "denominator"
            print denominator
            
            Sum=Sum+Weights[i]*Weights[j]*numpy.sqrt(numerator/denominator)
            print "Sum: " 
            print Sum 
    return Sum;
        
def TotalDistance(Weights,Means,CovarianceMatrices,Weights_Prime,Means_Prime,CovarianceMatrices_Prime):
    
    
    LeftPartDenominator=Denominator(Weights,Means,CovarianceMatrices)
    
    RightPartDenominator=Denominator(Weights_Prime,Means_Prime,CovarianceMatrices_Prime)

    return -numpy.log( 2*Numerator(Weights,Means,CovarianceMatrices,Weights_Prime,Means_Prime,CovarianceMatrices_Prime)/(LeftPartDenominator+RightPartDenominator))    

#End New Implementation
   
    


