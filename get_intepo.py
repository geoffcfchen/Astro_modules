from scipy import interpolate
from scipy.interpolate import RegularGridInterpolator
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
#matplotlib.interactive(True)


##oned_intepo is to intepolate 1d-histgram of a given array to a continous function. that is if one input 1-d array this function output the continuous function of the histgram of that 1-d array. It also return the edge of the prior.
def one_dim_intepo(x,x_bin='auto'):
    print(x.shape)
    (x_counts,x_bins,x_patches)=plt.hist(x, bins=x_bin,normed=True)
    x_counts=np.append(x_counts,0)
    x_dfference=x_bins[1]-x_bins[0]
    x_bins=x_bins+x_dfference/2.
    #plt.plot(x_bins,x_counts,'-')
    #plt.show()
    boundary_diff=0.0001*(x_bins[-1]-x_bins[0])
    print("the boundary diff is ", boundary_diff)
    print('the boundary of the paramter are',x_bins[0],x_bins[-1])
    print('the true return value are',x_bins[0]+boundary_diff,x_bins[-1]-boundary_diff)
    return interpolate.interp1d(x_bins,x_counts,kind='cubic'),x_bins[0]+boundary_diff,x_bins[-1]-boundary_diff

##threed_intepo is to intepolate 3d-histgram of a given 3-d array to a continous function. That is if one input 3-d array, this function output a continous function of the histgram of the 3-d array. The propose of threed_intepo is because the three parameters are not independent.
#The array type should look like
#array=((a,b,c),
#       (a,b,c),
#       (a,b,c))
#It also return the boundary (min,max) of parameter0,parameter1,parameter2
def three_dim_intepo(x,a=30,b=30,c=30):
    print("The dimension of the input array is",x.shape[1])
    print("The number of the data point in the input array is",x.shape[0])
    H, edges = np.histogramdd(x, bins = (a, b, c))
    H=H/np.sum(H)
    tmp=np.zeros((1,b,c))
    H0=np.concatenate((H,tmp),axis=0)
    tmp=np.zeros((a+1,1,c))
    H1=np.concatenate((H0,tmp),axis=1)
    tmp=np.zeros((a+1,b+1,1))
    H2=np.concatenate((H1,tmp),axis=2)
    a_dfference=edges[0][1]-edges[0][0]
    edges[0]=edges[0]+a_dfference/2
    b_dfference=edges[1][1]-edges[1][0]
    edges[1]=edges[1]+b_dfference/2
    c_dfference=edges[2][1]-edges[2][0]
    edges[2]=edges[2]+c_dfference/2
    boundary0_diff=0.0001*(edges[0][-1]-edges[0][0])
    boundary1_diff=0.0001*(edges[1][-1]-edges[1][0])
    boundary2_diff=0.0001*(edges[2][-1]-edges[2][0])
    print(boundary0_diff,boundary1_diff,boundary2_diff)
    print("the bins size of 0 axis, 1 axis, 2 axis are ",a,b,c)
    print('the boundary of paramter0 is',edges[0][0],edges[0][-1])
    print('the boundary of paramter1 is',edges[1][0],edges[1][-1])
    print('the boundary of paramter2 is',edges[2][0],edges[2][-1])
    print('the true return boundary of paramter0 is',edges[0][0]+boundary0_diff,edges[0][-1]-boundary0_diff)
    print('the true return boundary of paramter1 is',edges[1][0]+boundary1_diff,edges[1][-1]-boundary1_diff)
    print('the true return boundary of paramter2 is',edges[2][0]+boundary2_diff,edges[2][-1]-boundary2_diff)
    return RegularGridInterpolator((edges[0],edges[1],edges[2]), H2),edges[0][0]+boundary0_diff,edges[0][-1]-boundary0_diff,edges[1][0]+boundary1_diff,edges[1][-1]-boundary1_diff,edges[2][0]+boundary2_diff,edges[2][-1]-boundary2_diff
