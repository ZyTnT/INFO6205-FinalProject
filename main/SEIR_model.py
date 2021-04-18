import numpy as np

# This model is for test. It is used in calculator.py
#######################################################

def SEIR(inivalue, r, beta1, beta2, N, sigma, gamma):
    X = inivalue
    Y = np.zeros(4)
    # S number
    Y[0] = - (r * beta1 * X[0] * X[2]) / N - (r * beta2 * X[0] * X[1]) / N
    # E number
    Y[1] = (r * beta1 * X[0] * X[2]) / N + (r * beta2 * X[0] * X[1]) / N - sigma * X[1]
    # I number
    Y[2] = sigma * X[1] - gamma * X[2]
    # R number
    Y[3] = gamma * X[2]
    return Y