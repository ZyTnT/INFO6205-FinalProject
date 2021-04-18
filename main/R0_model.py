import math


# This is only for test, it is used in calculator.py
#######################################################
def R0Func(confirm, susceptible, t):

    Tg = 7
    Tl = 3
    Ti = Tg - Tl

    p = 0.695

    rho = Tl / Tg
    yt = susceptible * p + confirm
    lamda = math.log(yt) / (t + 1)
    R0 = 1 + lamda * Tg + rho * (1 - rho) * pow(lamda * Tg, 2)
    return R0
