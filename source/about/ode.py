h = 0.1
y0 = 1.0
x = 0.0

while x < 0.9:
    '''
    # Euler Implicit
    y1 = y0 + h * (y0 - 2 * x / y0)
    cnt = 10
    while cnt:
        y1 = y0 + h * (y1 - 2 * (x + h) / y1)
        cnt -= 1
    y0 = y1
    print(y0)
    x += h
    '''

    '''
    # Trapezoidal
    y1 = y0 + h * (y0 - 2 * x / y0)
    cnt = 10
    while cnt:
        y1 = y0 + (h / 2) * (y0 - 2 * x / y0 + y1 - 2 * (x + h) / y1)
        cnt -= 1
    y0 = y1
    print(y0)
    x += h
    '''
    '''
    # Fixed Euler
    yp = y0 + h * (y0 - 2.0 * x / y0)
    yc = y0 + h * (yp - 2.0 * (x + h) / yp)
    y1 = 0.5 * (yp + yc)
    print(y1)
    y0 = y1
    x += h
    '''

    # RK-3
    K1 = (y0 - 2 * x / y0)
    K2 = y0 + (h / 2) * K1 - 2 * (x + h / 2) / (y0 + (h / 2) * K1)
    K3 = y0 - h * K1 + 2 * h * K2 - 2 * (x + h) / (y0 - h * K1 + 2 * h * K2)
    y1 = y0 + (h / 6) * (K1 + 4 * K2 + K3)
    print(y1)
    y0 = y1
    x += h