#include <iostream>
#include <math.h>
#include <sys/time.h>
#include <fstream>
#include <assert.h>
using namespace std;
#define GET_LU_MAT 1
#define VERBOSE 0

enum {
    COL_MAJOR_ENABLED = 1,
    COL_MAJOR_DISABLED = 0,
    COL_MAJOR_LENGTH,
} COL_MAJOR;

template <typename T>
void print_AB(T** A, T* B, int N) {
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            printf("%011.7fx%d %c ", A[i][j], j, (j == N - 1) ? ' ' : '+');
        }
        printf("= %011.7f\n", B[i]);
    }
    std::cout << "----------------------" << std::endl;
}

template <typename T>
void swap_row(T** A, T*B, int N, int i, int j) {
    assert((i < N && j < N) && ("Swaping index exceeded!"));
    for (int k = 0; k < N; k++) {
        T tmp = A[i][k];
        A[i][k] = A[j][k];
        A[j][k] = tmp;
    }
    T tmp = B[i];
    B[i] = B[j];
    B[j] = tmp;
}

double elapsed_ms(const struct timeval& st, const struct timeval& ed) {
    return (1000000.0 * (ed.tv_sec - st.tv_sec) + (ed.tv_usec - st.tv_usec)) / 1000.0;
}

template <typename T>
void guassian(int N, int col_major) {
    struct timeval st, ed;
    T **A, *B;
    T *X;
    A = new T* [N];
    for (int i = 0; i < N; i++) {
        A[i] = new T [N];
    }
    B = new T [N];
    X = new T [N];

#if GET_LU_MAT == 1
    T **L, **U;
    L = new T *[N];
    U = new T *[N];
    for (int i = 0; i < N; i++) {
        L[i] = new T [N];
        U[i] = new T [N];
    }
#endif

    // Load from file
    ifstream fA("A", std::ios::in);
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            fA >> A[i][j];
        }
    }
    fA.close();

    ifstream fB("B", std::ios::in);
    for (int i = 0; i < N; i++) {
        fB >> B[i];
    }
    fB.close();
    gettimeofday(&st, NULL);
    // Step 1
    for (int i = 1; i < N; i++) {
        int col_pivot = i - 1;
        if (col_major == COL_MAJOR_ENABLED) {
            int idx = -1;
            T coeff_max = 1e-10;
            for (int m = i; m < N; m++) {
                if (abs(A[m][col_pivot]) > coeff_max) {
                    coeff_max = abs(A[m][col_pivot]);
                    idx = m;
                }
            }
            if (idx != i) swap_row(A, B, N, idx, i);
        }
        for (int j = i; j < N; j++) {
            T ratio = A[j][col_pivot] / A[i - 1][col_pivot];
            for (int k = col_pivot; k < N; k++) {
                A[j][k] = A[j][k] - ratio * A[i - 1][k]; 
            }
            B[j] = B[j] - ratio * B[i - 1];
        }
#if VERBOSE == 1
        print_AB(A, B, 4);
#endif
    }
    
    // Step 2
    for (int i = N - 1; i >= 0; i--) {
        T res = 0.0f;
        for (int j = i; j < N; j++) {
            res += A[i][j] * X[j];
        }
        X[i] = (B[i] - res) / A[i][i];
    }
    gettimeofday(&ed, NULL);
    std::cout << "Type = " << typeid(T).name() << ", " << "col major = " << col_major << " | ";
    std::cout << "X[0:" << N << "] = {";
    for (int i = 0; i < N; i++) printf("%09.6f%c", X[i], (i == N - 1) ? '\0' : ',');
    std::cout << "}, Time(ms) = ";
    std::cout << elapsed_ms(st, ed) << std::endl;
    
}

int main(int argc, char** argv) {
    int N = atoi(argv[1]);
    guassian<float>(N, COL_MAJOR_DISABLED);
    guassian<float>(N, COL_MAJOR_ENABLED);
    guassian<double>(N, COL_MAJOR_DISABLED);
    guassian<double>(N, COL_MAJOR_ENABLED);
}
