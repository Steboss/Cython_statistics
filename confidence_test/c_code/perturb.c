#include<stdio.h>
#include<stdlib.h>
#include<time.h>
#include<math.h>

double meanunsignederror(double *x, int len_x, double *y)
{
  double sumdev = 0.0 ;
  int i ;
  for(i=0;i<len_x;i++){
    sumdev+=fabs(x[i]-y[i]);
  }
  sumdev /=len_x;
  return sumdev;
}

double kendalT(double *x, int len_x, double * y, int len_y)
{
    //the two array MUST be have the same length
    int n2=0, n1=0, k, j;
    int is =0;
    double aa, a2, a1;

    for(j=1;j<len_x;j++){
      for(k=(j+1);k<=len_x;k++){
        a1=x[j]-x[k];
        a2=y[j]-y[k];
        aa = a1*a2;
        if (aa) {
          ++n1;
          ++n2;
          aa>0.0 ? ++is: --is;
        }
        else {
          if (a1) ++n1;
          if (a2) ++n2;
        }
      }
    }

    double tau;
    tau = is/(sqrt((double)n1)*sqrt((double)n2) );
    //printf("Tau is %.4f\n", tau);
    return tau;

}


double mean(double *x, int length){

  int i;
  double avg;
  //avg = 0.0;
  for(i=0; i<length;i++){
    if (i==0){
      avg = x[i];

    }
    else{
      avg = avg + (x[i]-avg)/i;
    }
  }
  return avg;
}


double PearsonR(double *x, int len_x, double *y, int len_y)
{

  //compute the mean for each array
  double mean_x, mean_y;
  mean_x = mean(x, len_x);
  mean_y = mean(y, len_y);
  double xt, yt, sxx, syy, sxy;
  //initialization
  sxx= 0.0;
  sxy = 0.0;
  syy = 0.0;

  int i;
  //
  //for(i=0;i<len_x;i++){
  //  printf("%.4f\n", x[i]);
  //}

  for(i=0;i<len_x;i++){
    xt = x[i]-mean_x;
    yt = y[i]-mean_y;
    sxx+=xt*xt;
    syy+=yt*yt;
    sxy+=xt*yt;
    //printf("Xt %.4f\n", xt);
  }
  //now take the pearson R
  double R ;
  R = sxy/(sqrt(sxx*syy));
  //printf("Correlation %.4f\n", pow(R,2));
  return R;

}



double boxMuller(double mean,double sigma){
  //set the seed
  //int seed = (int)time(NULL);
  //srand(seed);
  //rand();

  double two_pi =2*M_PI;

  double z1, u1,u2, z0;
  u1 = 0.0;
  while(u1==0.0){
    u1 = rand()*(1.0/RAND_MAX);
  }
  u2 = 0.0;
  while(u2==0.0){
    u2 = rand()*(1.0/RAND_MAX);
  }
  z1=sqrt(-2.0*log(u1))*cos(two_pi*u2);
  z0 = z1*sigma + mean;

  return z0;
}
/*
int main(){

  //FILE *ofile;
  //ofile =fopen("test.dat","w");

  double array1[10]={2,3,4,4,4,2,3,4,5,2};
  double array2[10]={2,4,4,2,4,2,6,1,4,1};
  meanunsignederror(array1,10,array2);
}*/
