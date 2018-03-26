# -*- coding: utf-8 -*-
import numpy as np
import  time
import sys
import rect_in

M = 100000000
N = 3

def in_boxes(boxes, points):
    # (N, 4, 2) = boxes.shape
    # (M, 2) = points.shape
    w = np.zeros(points.shape[0])
    start = time.time()
    for (i, point) in enumerate(points):
        in_box = False
        for box in boxes:
            (A, B, C, D) = box
            AP = (point - A)
            AB = (B - A)
            AD = (D - A)
            cond0 = 0 < np.dot(AP, AB) < np.dot(AB, AB)
            cond1 = 0 < np.dot(AP, AD) < np.dot(AD, AD)
            in_box = in_box or (cond0 and cond1)
        if in_box:
            w[i] = 1
        else:
            w[i] = 0

    end = time.time()
    print("Total time %.4fs" %(end-start))
    return w

#generate the boxes in a cartesian space xy
boxes = np.zeros((N,4,2))
#generate N boxes with 4 points of 2 coordinates
for i in range(0,N):
    x1 = np.random.randint(-10,10)
    x2 = np.random.randint(-10,10)
    x3 = np.random.randint(-10,10)
    x4 = np.random.randint(-10,10)
    y1 = np.random.randint(-10,10)
    y2 = np.random.randint(-10,10)
    y3 = np.random.randint(-10,10)
    y4 = np.random.randint(-10,10)
    boxes[i][0] = (x1,y1)
    boxes[i][1] = (x2,y2)
    boxes[i][2] = (x3,y3)
    boxes[i][3] = (x4,y4)

#generate M points in xy from -10 to +10 for both coordinates
points = np.zeros((M,2))
for i in range(0,M):
    x = np.random.randint(-10,10)
    y = np.random.randint(-10,10)
    points[i]=(x,y)

#print(boxes.shape)

start = time.time()
rect_in.rectangle(boxes, points)
end = time.time()
print(end-start)
sys.exit(-1)
