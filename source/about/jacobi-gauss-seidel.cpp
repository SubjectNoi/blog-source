#include <iostream>
#include <fstream>
#define GAUSS_SEIDEL 1 
using namespace std;

template <typename T>
void read_mat(T** mat, int M, int N, const char* path) {
    std::ifstream fin(path, std::ios::in);
    for (int i = 0; i < M; i++) {
        for (int j = 0; j < N; j++) {
            fin >> mat[i][j];
        }
    }
    fin.close();
}

int main(int argc, char** argv) {
    int N = atoi(argv[1]);
    int iter = atoi(argv[2]);
    double sor_omega = atof(argv[3]);
    double err_bound = atof(argv[4]);
    double **A, **b, **ref, *x, *tmp;
    A = new double*[N];
    b = new double*[N];
    ref = new double*[N];
    x = new double[N];
    tmp = new double[N];
    for (int i = 0; i < N; i++) {
        A[i] = new double[N];
        b[i] = new double[1];
        ref[i] = new double[1];
    }

    read_mat(A, N, N, "A");
    read_mat(b, N, 1, "B");
    read_mat(ref, N, 1, "ref");
    for (int i = 0; i < N; i++) {
        x[i] = 0.5;
    }
    for (int k = 0; k < iter; k++) {
        for (int i = 0; i < N; i++) tmp[i] = x[i];
        for (int i = 0; i < N; i++) {
            double res = 0.0f;
            for (int j = 0; j < N; j++) {
                if (j == i) continue;
#if GAUSS_SEIDEL == 1
                res += A[i][j] * x[j];
#else
                res += A[i][j] * tmp[j];
#endif
            }
#if GAUSS_SEIDEL == 1
            x[i] = (1 - sor_omega) * tmp[i] + sor_omega * (b[i][0] - res) / A[i][i];
#else
            x[i] = (b[i][0] - res) / A[i][i];
#endif
        }
        printf("[%04d] X = ", k);
        for (int i = 0; i < N; i++) {
            printf("% 010.7f[%d]%c", x[i], abs(x[i] - ref[i][0]) < err_bound, (i == N - 1) ? '\n' : ',');
        }
    }
}
