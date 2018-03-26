#include<stdio.h>
#include<stdlib.h>
#include<time.h>
#include<math.h>
#include "rectangle.h"
//compute the dot product
double dot_product(double segment1[2], double segment2[2])
{
  double result = 0.0;
  int s;
  for(s=0;s<2;s++)
  {
    result+= segment1[s]*segment2[s];
  }
  return result;
}

int in_rect(double *boxes, int n_boxes,int n_boxes_coords, double *points, int n_points)
{

  int counter = 0 ;
  int i,j,k;
  /*
  Here we could cycle through the first box, retrieve the coords of Axy,B,C,D
  into arrays or one array?
  then cycle through th epoints and compute Ax - pointX, Ay - pointY
  */
  double *edges ;
  edges = malloc(sizeof(double));
  double pointX;
  double pointY;
  double AP[2];
  double AB[2];
  double AD[2];
  double cond0;
  double cond1;
  double cond2;
  double cond3;
  int within =0 ;
  /*cycle through all the boxes*/
  printf("Counting how many points are within...\n");
  for(i=0;i<n_boxes;i++)
  {
    /*retrieve the coords*/
    printf("Processing box n. %d\n",i);
    for (j=0;j<n_boxes_coords;j+=2)
    {
      edges[j] = boxes[j];
      edges[j+1] = boxes[j+1];
    }
    //now 0,1 is A, 2,3 B, 4,5 C 6,7 D
    //cycle thorugh the points
    //compute here AB, AD
    AB[0] = edges[2]-edges[0];
    AB[1] = edges[3]-edges[1];
    AD[0] = edges[6]-edges[0];
    AD[1] = edges[7]-edges[1];

    for(k=0;k<n_points;k+=2)
    {
      pointX = points[k];
      pointY = points[k+1];
      //compute AP
      AP[0] = pointX - edges[0];
      AP[1] = pointY - edges[1];
      //check if the pointis within the box
      cond0 = dot_product(AP,AB);
      cond1 = dot_product(AB,AB);
      cond2 = dot_product(AP,AD);
      cond3 = dot_product(AD,AD);
      if (cond0>0 && cond0<cond1)
      {
        if (cond2>0 && cond2<cond3)
        {
          within+=1;
        }
        else{
          within+=0;
        }
      }
      //printf("%d\n",within);


    }
  }
  //free(edges);
  printf("Calculation completed\n");
  printf("%d\n",within);
  //exit(0);
}
/*
int main()
{
  double *boxes ;
  boxes = malloc(sizeof(double));
  double *points ;
  points = malloc(sizeof(double));
  int i,j ;
  for (i=0;i<3;i++)
  {
    for(j=0;j<8;j++)
    {
      boxes[j] =1;
    }
  }
  for (i=0;i<10;i+=2)
  {
    points[i]=1;
    points[i+1]=2;
  }

  in_rect(boxes,3,8,points,10);
}*/
