void saxpy(int n, const float a, const float *x, float *y)
{
   int i;
   for (i=0; i<n; i++)
     y[i] = a * x[i] + y[i];
}