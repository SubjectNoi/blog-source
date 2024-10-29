#include <iostream>
#include <fstream>
#include <vector>
#include <array>
using namespace std;

void generate_diff_quo_table(const vector<double>& X, const vector<double>& Y, int N, double** tbl) {
    for (int i = 0; i < N; i++) tbl[i][0] = Y[i];
    for (int i = 1; i < N; i++) {
        for (int j = 1; j <= i; j++) {
            tbl[i][j] = (tbl[i][j - 1] - tbl[i - 1][j - 1]) / (X[i] - X[i - j]);
        }
    }
}

int main(int argc, char** argv) {
    int st = atoi(argv[1]); 
    int ed = atoi(argv[2]);
    int total = atoi(argv[3]);
    int N = ed - st + 1;
    double x_star = atof(argv[4]);
    vector <double> XX, YY;
    ifstream fin("XY", std::ios::in);
    for (int i = 0; i < total; i++) {
        double _x, _y;
        fin >> _x >> _y;
        XX.push_back(_x);
        YY.push_back(_y);
    }
    vector <double> X, Y;
    for (int i = st; i <= ed; i++) {
        X.push_back(XX[i]);
        Y.push_back(YY[i]);
    }
    double **T;
    T = new double*[N];
    for (int i = 0; i < N; i++) T[i] = new double[N];
    generate_diff_quo_table(X, Y, N, T);
    double res = 0.0;
    for (int i = 0; i < N; i++) {
        double m = 1.0, n = 1.0;
        for (int j = 0; j < N; j++) {
            if (j != i) {
                m *= (x_star - X[j]);
                n *= (X[i] - X[j]);
            }
        }
        res += Y[i] * (m / n);
    }
    printf("Lagrange: %010.7f\n", res);

    double newton_res = T[0][0];
    double omega = 1.0;
    for (int i = 1; i < N; i++) {
        omega *= (x_star - X[i - 1]);
        newton_res += T[i][i] * omega;
    }
    printf("  Newton: %010.7f\n", newton_res);
    return 0;
}
