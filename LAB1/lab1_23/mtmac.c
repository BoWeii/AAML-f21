// This file is for extend ISA "mtmac" .

#include <stdio.h>
void *tensormul(size_t n, const int *x, const int *y, int *z);
int main(int argc, char **argv)
{
#define N 16

  const int x[N] = {2, 1, 3, 4,
                    5, 2, 7, 3,
                    3, 2, 5, 1,
                    1, 7, 3, 2};
  const int y[N] = {5, 3, 4, 2,
                    3, 1, 7, 1,
                    2, 5, 4, 1,
                    4, 1, 3, 3};
  int z[N] = {1, 1, 1, 1,
              1, 1, 1, 1,
              1, 1, 1, 1,
              1, 1, 1, 1};
  tensormul(N, x, y, z);
  for (int i = 0; i < N; i++)
  {
    printf("%d ", z[i]);
  }
  printf("\n");
}
