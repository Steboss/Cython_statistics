#include<stdio.h>
#include<stdlib.h>
#include<time.h>
#include<math.h>

double meanunsignederror(double *x, int len_x, double *y);
double kendalT(double *x, int len_x, double * y, int len_y);
double mean(double *x, int length);
double PearsonR(double *x, int len_x, double *y, int len_y);
double boxMuller(double mu, double sigma);
