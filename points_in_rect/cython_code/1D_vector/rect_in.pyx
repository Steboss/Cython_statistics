#cython: boundscheck=False
#cython: wraparound=False
#cython: nonecheck=False

import re,sys
cimport numpy as np
cimport cython
from cython.parallel import parallel, prange

cdef extern from "c_code/rectangle.c":
  int in_rect(double *boxes, int n_boxes,int n_boxes_coords, double *points, int n_points)


cpdef rectangle(np.ndarray[double, ndim=3, mode="c"] boxes,
               np.ndarray[double, ndim=2, mode="c"] points):
  #as input we have 2 arrays, one with the boxes  cartesian coords
  #the other with points cartesian coords (2D)
  #mode C ensure you have a one D array
  #boxes and points generated in python
  #now we need C to compute the number of points within the rectangle
  #transform into memory view the arrays
  B, M = boxes.shape[0], boxes.shape[1]*2  #B number of rectangles, M rect coords
  N, y = points.shape[0], points.shape[1]

  #cdef double** boxes_pointers = <double **>malloc(M * sizeof(double*))
  #fill the pointer
  #::1 ensures contigousness
  cdef double[:,:,::1] boxes_view = boxes
  cdef double[:,::1] points_view = points

  in_rect(&boxes_view[0,0,0], B, M, &points_view[0,0], N)
