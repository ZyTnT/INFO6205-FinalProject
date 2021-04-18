import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as spi
import math


#########################################################################################
#   multiple_factor_calculator() Configure:
#
#   N: Total population of the area.
#   S_0: Initial susceptible number.
#   E_0: Initial Exposed number.
#   I_0: Initial infected number.
#   recovery: Initial removed number.
#   confirmTime: Total time from infected to confirm.
#   latentTime: Total time from infected to infectious.
#   r:The average number of a person meet everyday. (Home quarantine will decrease it)
#   T: Total days for simulation.
#   afterDays: Days before government makes policies (Default value is 0 if no input.)
#   methods: list of government policies(30% vaccine, 50%vaccine, 70%vaccine, home, mask)
#############################################################################################


def multiple_factors_calculator(N, S_0, E_0, I_0, recovery, confirmTime, latentTime, r, T, afterDays, methods: list):
    #   S\E\I\R calulator for iteration.
    def SEIR(inivalue, _):
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

    #       R0 calculator based on S\E\I\R everyday
    def R0Func(confirm, susceptible, t):
        # confirm is total confirm population；susceptible is total susceptible population, t is the number of days from start.

        # Tg：time from infected to confirm
        Tg = confirmTime
        # Tl —— latentTime: time from infected to infectious
        Tl = latentTime
        # Ti: time that can infectious
        Ti = Tg - Tl

        # p is the probability that Exposed become confirm.
        p = 0.695
        # rho is the over incubation period over generation time

        rho = Tl / Tg
        # yt actual infected population
        yt = susceptible * p + confirm
        # lamda is growth rate of exponential growth in early period.
        lamda = math.log(yt) / (t + 1)
        R0 = 1 + lamda * Tg + rho * (1 - rho) * pow(lamda * Tg, 2)
        return R0

    beta1 = 0.05  # The probability that a infected person infect susceptible. I -> S. (Based on real medical data)
    beta2 = 0.02  # The probability that a exposed person infect susceptible. E -> S. (Based on real medical data)
    sigma = 1 / latentTime # The probability that a exposed person become infected. E -> I.
    gamma = 1 / (confirmTime - latentTime) # The probability that a infected person become removed. (recovery or death)
    R_0 = recovery
    K = beta2 * (confirmTime - latentTime)
    if afterDays is None:
        afterDays = 0

    start_INI = [S_0, E_0, I_0, R_0]
    T_range1 = np.arange(0, afterDays + 1) # Total days before government make policies.
    T_range2 = np.arange(0, T - afterDays) # Total days after government make policies.

    Res1 = spi.odeint(SEIR, start_INI, T_range1) # Iteration for everyday data.
    S_t1 = Res1[:, 0]
    E_t1 = Res1[:, 1]
    I_t1 = Res1[:, 2]
    R_t1 = Res1[:, 3]

    # Get the last day data for next iteration.
    S_t2 = S_t1[afterDays]
    E_t2 = E_t1[afterDays]
    I_t2 = I_t1[afterDays]
    R_t2 = R_t1[afterDays]

    # change configures based on government configures.
    if methods is not None:
        for method in methods:
            if method == '30%vaccine':
                S_t2 = 0.7 * S_t2
            elif method == '50%vaccine':
                S_t2 = 0.5 * S_t2
            elif method == '70%vaccine':
                S_t2 = 0.3 * S_t2
            if method == 'testing':
                confirmTime = 0.7*confirmTime
                gamma = 1 / (confirmTime - latentTime)
            if method == 'home':
                r = 2
            if method == 'mask':
                beta1 = 0.6 * beta1
                beta2 = 0.6 * beta2

    # Iteration
    INI2 = [S_t2, E_t2, I_t2, R_t2]
    Res2 = spi.odeint(SEIR, INI2, T_range2)
    S_t3 = Res2[:, 0]
    E_t3 = Res2[:, 1]
    I_t3 = Res2[:, 2]
    R_t3 = Res2[:, 3]

    # Change the data type of two periods and merge.
    S_t1 = list(S_t1)
    S_t3 = list(S_t3)
    E_t1 = list(E_t1)
    E_t3 = list(E_t3)
    I_t1 = list(I_t1)
    I_t3 = list(I_t3)
    R_t1 = list(R_t1)
    R_t3 = list(R_t3)

    S_t = S_t1 + S_t3
    E_t = E_t1 + E_t3
    I_t = I_t1 + I_t3
    R_t = R_t1 + R_t3

    S_t = np.array(S_t)
    E_t = np.array(E_t)
    I_t = np.array(I_t)
    R_t = np.array(R_t)

    # Calculate everyday R0 and store in a list.
    reproductionList = []
    for i in range(len(S_t)):
        R = R0Func(I_t[i], S_t[i], i)
        reproductionList.append(R)

    return S_t, E_t, I_t, R_t, reproductionList


#########################################################################################
#   R0_calculator() Configure:
#
#   N: Total population of the area.
#   S_0: Initial susceptible number.
#   E_0: Initial Exposed number.
#   I_0: Initial infected number.
#   recovery: Initial removed number.
#   R0: Basic reproduction number.
#   T: Total days for simulation.
###########################################################################################


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

    # Tg：Total time from infected to confirm.
    Tg = 7
    # Tl: Total time from infected to infectious.
    Tl = 3
    # Ti: Infectious time
    Ti = Tg - Tl

    # beta is effective contact rate
    def betaFunc(R0=R0, Ti=Ti):
        return R0 / Ti

    # gamma is removal rate
    def gammaFunc(Tg=Tg):
        return 1 / Tg

    gamma = gammaFunc()
    beta = betaFunc(R0)

    # Iteration
    INI = (S_0, E_0, I_0, R_0)
    Res = spi.odeint(SEIR, INI, T_range)
    S_t2 = Res[:, 0]
    E_t2 = Res[:, 1]
    I_t2 = Res[:, 2]
    R_t2 = Res[:, 3]

    return S_t2, E_t2, I_t2, R_t2
