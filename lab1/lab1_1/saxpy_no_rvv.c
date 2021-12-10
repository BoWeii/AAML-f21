#include <stdbool.h>
#include <stdio.h>

void *saxpy_no_rvv(size_t n, const float a, const float *x, float *y);

void test_saxpy() {
  #define N 7
  const float x[N] = {7, 7, 7, 7, 7, 7, 7};
        float y[N] = {1, 1, 1, 1, 1, 1, 1};
  const float z[N] = {15, 15, 15, 15, 15, 15, 15};
  const float a = 2;

  printf(">>> Testing saxpy.s...\n");
  printf(">>> x = ");
  for (int i = 0; i < N; i++)
    printf("%f, ", x[i]);
  printf("\n");

  printf(">>> y = ");
  for (int i = 0; i < N; i++)
    printf("%f, ", y[i]);
  printf("\n");

  printf(">>> a = %f\n", a);

  printf(">>> after calling saxpy(%d, a, x, y)\n", N);
  saxpy_no_rvv(N, a, x, y);

  printf(">>> y = ");
  for (int i = 0; i < N; i++)
    printf("%f, ", y[i]);
  printf("\n");

  /* Check result. */
  bool status = true;
  for (int i = 0; i < N; ++i) {
    if (y[i] != z[i]) {
      status = false;
      break;
    }
  }
  printf(">>> %s\n\n", status ? "Pass!" : "Failed!");
  #undef N
}

int main(void)
{
  printf("\nRunning saxpy...\n");
  test_saxpy();//You have to finish saxpy.s to run this function.
}
