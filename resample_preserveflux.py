import numpy as np
from get_intepo import one_dim_intepo
from matplotlib import pyplot as plt
from scipy import ndimage

#samples=np.random.normal(10,2,10000)
#plt.hist(samples)
#plt.show()
#distribution, x_min, x_max =one_dim_intepo(samples)

#x_axis=np.linspace(x_min,x_max,100)
#y_axis=distribution(x_axis)
#plt.plot(y_axis)
#plt.show()


def resample_1D_prevflux(array,pixel_size,new_pixel_size):
    """

    :param array: input 1D array
    :param pixel_size: the pixel size of the 1D array
    :param new_pixel_size: the new pixel size for the output 1D array
    :return: new 1D array which preserve the flux, and the corresponding matrix
    """
    array=array#np.arange(31)#array#np.array([0,1,2]) ## example chains
    N = array.shape[0]
    array=np.append(array,0.)
    pixel_size= pixel_size #10.  ##old pixel size
    axis_dis=np.linspace(0,pixel_size*(N+1),N+2)  #create the locations for the
    # pixel boundary in old array and create one extra pixel
    new_pixel_size= new_pixel_size #6.  # new pixel size
    total_length=pixel_size*N
    N_new = int(pixel_size * N / new_pixel_size)+2
    new_axis_dis = np.arange(N_new)*new_pixel_size #create the
    #  locations for the pixel boundary in new array
    new_array=np.zeros(N_new-1)
    matrix=np.zeros((new_array.shape[0],N+1))
    #print(matrix.shape)
    for i in range(new_array.shape[0]):
        # this is to identify if new pixel is located completely inside the
        # old pixel
        if all(np.sort(np.argsort(np.abs(axis_dis-new_axis_dis[i]))[:2]) == \
                np.sort(np.argsort(np.abs(axis_dis-new_axis_dis[i+1]))[:2])):
            ind_in_oldarray=np.sort(np.argsort(np.abs(axis_dis-new_axis_dis[
                i]))[:1])[0]
            #print(ind_in_oldarray)
            new_array[i] = new_pixel_size / pixel_size * array[ind_in_oldarray]
            matrix[i,ind_in_oldarray]= new_pixel_size / pixel_size
            #print("locate inside",i)
        # this is to identify if new pixel is located partially inside the
        # new pixel
        elif all(np.sort(np.argsort(np.abs(axis_dis-new_axis_dis[i]))[:2]) !=\
                np.sort(np.argsort(np.abs(axis_dis-new_axis_dis[i+1]))[:2])):
            ind_in_oldarray_1=np.sort(np.argsort(np.abs(
                axis_dis-new_axis_dis[i]))[:2])[0]
            ind_in_oldarray_2=np.sort(np.argsort(np.abs(
                axis_dis-new_axis_dis[i+1]))[:2])[0]
            #print(ind_in_oldarray_1,ind_in_oldarray_2)
            old_array_value_center=axis_dis[ind_in_oldarray_1+1]
            ratio1=abs((new_axis_dis[i]-old_array_value_center)/pixel_size)
            ratio2 = abs(
                (new_axis_dis[i+1] - old_array_value_center) / pixel_size)
            new_array[i] = ratio1* array[ind_in_oldarray_1]+ratio2* array[
                ind_in_oldarray_2]
            matrix[i,ind_in_oldarray_1]=ratio1
            matrix[i,ind_in_oldarray_2]=ratio2
            #print("locate parial", i)
        else:
            print("something wrong")
    matrix=np.delete(matrix, -1, axis=1) ##remove last column
    return new_array, matrix


##for testing if it is flux preserved
#new_y,matrix=resample_1D_prevflux(y_axis,1,0.44)
#np.sum(y_axis)
#np.sum(new_y)