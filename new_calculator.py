import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as spi
import math
from pandas import DataFrame as df


def multiple_factor_calculator(N,S_0, E_0,I_0,recovery,confirmTime, latentTime,r,T, methods:list):

    beta1 = 0.78735
    beta2 = 0.15747
    sigma = 1/latentTime
    gamma = 1/(confirmTime-latentTime)
    R_0 = recovery
    if methods is not None:
        for method in methods:
            if method == '30%vaccine':
                S_0 = 0.7*S_0
            elif method == '50%vaccine':
                S_0 = 0.5*S_0
            elif method == '70%vaccine':
                S_0 = 0.3*S_0
            if method == 'home':
                r = 1
            if method == 'mask':
                beta1 = 0.6*beta1
                beta2 = 0.6*beta2

    INI = [S_0, E_0, I_0, R_0]
    T_range = np.arange(0, T + 1)



    def SEIR(inivalue, _):
        X = inivalue
        Y = np.zeros(4)
        # S数量
        Y[0] = - (r * beta1 * X[0] * X[2]) / N - (r * beta2 * X[0] * X[1]) / N
        # E数量
        Y[1] = (r * beta1 * X[0] * X[2]) / N + (r * beta2 * X[0] * X[1]) / N - sigma * X[1]
        # I数量
        Y[2] = sigma * X[1] - gamma * X[2]
        # R数量
        Y[3] = gamma * X[2]
        return Y

    def R0Func(confirm, suspect, t):
        # confirm是确诊人数；susp是疑似人数；t是疾病已爆发时间

        # Tg：从感染到发病
        Tg = confirmTime
        # Tl:潜伏期，从感染到开始传播
        Tl = latentTime
        # Ti:传播期
        Ti = Tg - Tl

        # p为疑似病例转化为确诊病例的概率
        p = 0.695
        # rho is the over incubation period over generation time

        rho = Tl / Tg
        # yt为实际预估感染人数
        yt = suspect * p + confirm
        # lamda为早期指数增长的增长率
        lamda = math.log(yt) / (t+1)
        R0 = 1 + lamda * Tg + rho * (1 - rho) * pow(lamda * Tg, 2)
        return R0

    Res = spi.odeint(SEIR, INI, T_range)
    S_t2 = Res[:, 0]
    E_t2 = Res[:, 1]
    I_t2 = Res[:, 2]
    R_t2 = Res[:, 3]

    reproductionList = []
    for i in range(len(S_t2)):
        R = R0Func(I_t2[i], S_t2[i], i)
        reproductionList.append(R)

    return S_t2, E_t2, I_t2, R_t2


def R0_calculator(N, S_0, E_0, I_0, recovery, R0, T):
    R_0 = recovery

    def SEIR(inivalue, _):
        Y = np.zeros(4)
        X = inivalue
        # dS/dt
        Y[0] = - (beta * X[0] * X[2]) / N
        # dE/dt
        Y[1] = (beta * X[0] * X[2]) / N - X[1] / Tg
        # dI/dt
        Y[2] = X[1] / Tg - gamma * X[2]
        # dR/dt
        Y[3] = gamma * X[2]
        return Y

    T_range = np.arange(0, T + 1)
    # R0 is basic reproduction number

    # Tg：从感染到发病
    Tg = 7.5
    # Tl:潜伏期，从感染到开始传播
    Tl = 3
    # Ti:传播期
    Ti = Tg - Tl

    # beta is effective contact rate
    def betaFunc(R0=R0, Ti=Ti):
        return R0 / Ti

    # gamma is removal rate
    def gammaFunc(Tg=Tg):
        return 1 / Tg

    gamma = gammaFunc()
    beta = betaFunc(R0)

    INI = (S_0, E_0, I_0, R_0)
    Res = spi.odeint(SEIR, INI, T_range)
    S_t2 = Res[:, 0]
    E_t2 = Res[:, 1]
    I_t2 = Res[:, 2]
    R_t2 = Res[:, 3]

    return S_t2, E_t2, I_t2, R_t2


if __name__ == '__main__':
    N = 1000000  # 湖北省为6000 0000
    E_0 = 0
    I_0 = 100
    R_0 = 0
    S_0 = N - E_0 - I_0 - R_0
    beta1 = 0.78735  # 真实数据拟合得出
    beta2 = 0.15747
    # r2 * beta2 = 2
    sigma = 1 / 14  # 1/14, 潜伏期的倒数
    gamma = 1 / 7  # 1/7, 感染期的倒数
    r = 0.5  # 政府干预措施决定
    T = 150
    R0 = 100

    S_t, E_t, I_t, R_t = R0_calculator(N,E_0,I_0,R0)
    #reproductionList = np.array(reproductionList)
    plt.plot(S_t, color='blue', label='Susceptibles')#, marker='.')
    plt.plot(E_t, color='grey', label='Exposed')
    plt.plot(I_t, color='red', label='Infected')
    plt.plot(R_t, color='green', label='Recoverd')
    #plt.plot(reproductionList, color='yellow', label='Reproduction Number')
    plt.xlabel('Day')
    plt.ylabel('Number')
    plt.title('SEIR Model')
    plt.legend()
    plt.show()