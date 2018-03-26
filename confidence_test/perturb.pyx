#cython: boundscheck=False
#cython: wraparound=False
#cython: nonecheck=False

import cython

cdef extern from "c_code/perturb.c":
    double boxMuller(double mu,double sigma)
    double mean(double *x, int len_x)
    double PearsonR(double *x, int len_x, double *y, int len_y)
    double kendalT(double *x, int len_x, double * y, int len_y);
    double meanunsignederror(double *x, int len_x, double *y);


cpdef double mue(python_array1,python_array2):
    len_x = len(python_array1)
    cdef double[:] memory_1 = python_array1
    cdef double[:] memory_2 = python_array2
    mean_err = meanunsignederror(&memory_1[0],len_x,&memory_2[0])
    return mean_err

cpdef double kendaltau(python_array1,python_array2):
    len_x = len(python_array1)
    cdef double[:] memory_1 = python_array1
    cdef double[:] memory_2 = python_array2

    t = kendalT(&memory_1[0],len_x,&memory_2[0],len_x)
    return t


cpdef double perturbation(double x, double y):
    cdef double result
    result =(boxMuller(x,y))
    return result

cpdef double average(python_array):
    len_x = len(python_array)
    cdef double[:] memory_array = python_array
    #len_x= python_array.shape[0]
    cdef double avg
    avg = 0.0
    avg = mean(&memory_array[0],len_x)
    #print("The average is %.4f\n" % avg)
    return avg

cpdef double correlation(python_array1,python_array2):
    len_x = len(python_array1)
    len_y = len(python_array2)
    cdef double[:] memory_1 = python_array1
    cdef double[:] memory_2 = python_array2
    r = PearsonR(&memory_1[0], len_x, &memory_2[0], len_y)
    #print(r)
    #print("Pearson %.4f" % r)
    #print("R^2 %.4f" % r**2)
    return r
