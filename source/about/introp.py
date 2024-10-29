import matplotlib.pyplot as plt
import math
import sys
import numpy as np

MM = {"spline" : 'x', "lagrange" : '+', "seg-linear": "."}

def f(x):
    return 1 / (1 + x ** 2)
    # return math.log(x)

def generate_cheb(func, a, b, n, bound=1):
    xk, yk = [], []
    for i in range(1, n + 1):
        xk.append(bound * math.cos((2 * i - 1) * math.pi / (2 * n)))
    yk = [func(x) for x in xk]
    return xk, yk

def generate_lag(func, a, b, n, bound=1):
    xk, yk = [], []
    for i in range(0, n + 1):
        xk.append(a + (bound * i / n))
    yk = [func(x) for x in xk]
    return xk, yk

def gen_diff_quo_tbl(XY):
    N = len(XY)
    T = np.zeros(shape=(N, N))
    X = [x[0] for x in XY]
    Y = [x[1] for x in XY]
    for i in range(N):
        T[i][0] = Y[i]
    for i in range(1, N):
        for j in range(1, i + 1):
            T[i][j] = (T[i][j - 1] - T[i - 1][j - 1]) / (X[i] - X[i - j])
    return T

def introp(func, XY, cond_val, xmin=-5, xmax=5, n_introp=50001, type='lagrange', cond='1', cheb=False):
    if func != None:
        xx = np.linspace(xmin, xmax, int((xmax - xmin) * 1000))
        yy = [f(x) for x in xx]
        plt.plot(xx, yy, linestyle='--', linewidth=5, c='black', alpha=0.1, label='reference')
        plt.xlim(xmin, xmax)
        plt.xticks(range(xmin, xmax + 1, 1))
    else:
        x = [x[0] for x in XY]
        y = [x[1] for x in XY]
        plt.scatter(x, y)
    if type not in {'lagrange', 'seg-linear', 'spline'}:
        print(f"Type:{type} not supported.")
    if cond not in {'1', '2'}:
        print(f"Cond:{type} not supported.")
    n_points = len(XY)
    to_introp_x = []
    to_introp_y = []
    step = (xmax - xmin) / (n_introp - 1)
    for i in range(n_introp):
        to_introp_x.append(xmin + i * step)
    if type == 'lagrange':
        T = gen_diff_quo_tbl(XY)
        X = [x[0] for x in XY]
        Y = [x[1] for x in XY]
        for x in range(n_introp):
            res = 0.0
            for i in range(n_points):
                m, n = 1.0, 1.0
                for j in range(n_points):
                    if j != i:
                        m *= (to_introp_x[x] - X[j])
                        n *= (X[i] - X[j])
                res += Y[i] * (m / n)
            to_introp_y.append(res)
    elif type == 'seg-linear':
        X = [x[0] for x in XY]
        Y = [x[1] for x in XY]
        for x in range(n_introp):
            idx = -1
            for xx in range(n_points):
                if to_introp_x[x] > X[xx]:
                    idx = xx
            x0, y0 = X[idx], Y[idx]
            x1, y1 = X[idx + 1], Y[idx + 1]
            res = y0 * (to_introp_x[x] - x1) / (x0 - x1) + y1 * (to_introp_x[x] - x0) / (x1 - x0)
            res -= 0.005
            to_introp_y.append(res)
    elif type == 'spline':
        dx0, ddx0 = 0.0, 0.0
        dxn, ddxn = 0.0, 0.0
        cx0, cxn = cond_val[0], cond_val[1]
        if cond == '1':
            dx0 = cx0
            dxn = cxn
        X = [x[0] for x in XY]
        Y = [x[1] for x in XY]
        d = [0 for i in range(n_points)]
        h = []
        for i in range(n_points - 1):
            h.append(X[i + 1] - X[i])
        MU = [0 for i in range(n_points)]
        LAMBDA = [0 for i in range(n_points)]
        LAMBDA[0] = 1
        MU[n_points - 1] = 1
        for i in range(1, n_points - 1):
            MU[i] = (h[i - 1]) / (h[i - 1] + h[i])
            LAMBDA[i] = (h[i]) / (h[i - 1] + h[i])
            d[i] = 6 * (((Y[i + 1] - Y[i]) / (X[i + 1] - X[i])) - ((Y[i] - Y[i - 1]) / (X[i] - X[i - 1]))) / (h[i - 1] + h[i])
        d[0] = 6 * ((Y[1] - Y[0]) / (X[1] - X[0]) - dx0) / (X[1] - X[0])
        d[n_points - 1] = 6 * (dxn - (Y[n_points - 1] - Y[n_points - 2]) / (X[n_points - 1] - X[n_points - 2])) / (X[n_points - 1] - X[n_points - 2])
        A = np.zeros(shape=(n_points, n_points))
        B = np.zeros(shape=(n_points, 1))
        for i in range(n_points):
            B[i] = d[i]
            A[i][i] = 2.0
        for i in range(n_points - 1):
            A[i][i + 1] = LAMBDA[i]
        for i in range(1, n_points):
            A[i][i - 1] = MU[i]
        M = np.linalg.solve(A, B)

        for x in range(n_introp):
            idx = -1
            for xx in range(n_points):
                if to_introp_x[x] > X[xx]:
                    idx = xx
            x_star = to_introp_x[x]
            res = M[idx] * (X[idx + 1] - x_star) ** 3 / (6 * h[idx]) + M[idx + 1] * (x_star - X[idx]) ** 3 / (6 * h[idx]) + (Y[idx] - (M[idx] * h[idx] ** 2) / 6) * ((X[idx + 1] - x_star) / h[idx]) + (Y[idx + 1] - (M[idx + 1] * h[idx] ** 2) / 6) * ((x_star - X[idx]) / h[idx])
            to_introp_y.append(res)
        for i in range(n_introp):
            if to_introp_x[i] in X:
                idx = X.index(to_introp_x[i])
                if idx != -1:
                    to_introp_y[i] = Y[idx]
        to_introp_y = [x + 0.005 for x in to_introp_y]
    else:
        pass

    plt.scatter(to_introp_x, to_introp_y, s=50000 / n_introp, label=type + ("(cheb)" if cheb else " "), marker=MM[type], alpha=0.1)
    # plt.show()
    

if __name__ == "__main__":
    # x, y = generate_lag(f, -5, 5, 50, 10)
    # for i in range(len(x)):
    #     print(x[i], y[i])
    
    fxy = open("XY").readlines()
    fxy_non_cheb = open("XY").readlines()
    fcond = open("cond").readlines()
    XY = []
    XY_non_cheb = []
    cond_val = []
    for item in fxy:
        tmp = [float(x) for x in item.split("\n")[0].split()]
        XY.append([tmp[0], tmp[1]])
    for item in fxy_non_cheb:
        tmp = [float(x) for x in item.split("\n")[0].split()]
        XY_non_cheb.append([tmp[0], tmp[1]])
    for item in fcond:
        cond_val.append(float(item))
    introp(f, XY, cond_val, xmin=-5, xmax=5, type='spline', cond='1')
    # introp(f, XY, cond_val, xmin=-5, xmax=5, type='lagrange', cond='1', cheb=True)
    introp(f, XY_non_cheb, cond_val, xmin=-5, xmax=5, type='lagrange', cond='1')
    introp(f, XY, cond_val, xmin=-5, xmax=5, type='seg-linear', cond='1')
    plt.ylim(-0.5, 1)
    plt.legend()
    plt.show()
    

