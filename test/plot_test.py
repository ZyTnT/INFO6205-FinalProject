import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as spi

# First period，11.24 - 1.23  1.11
N = 60000000    # Wuhan population
E_0 = 0
I_0 = 1
R_0 = 0
S_0 = N - E_0 - I_0 - R_0
beta1 = 0.02
beta2 = 0.021/3      #0.007
# r2 * beta2 = 2
sigma = 1/14
gamma = 1/7
r = 18
T = 74

#ode求解
INI = [S_0, E_0, I_0, R_0]
def SEIR(inivalue, _):
    X = inivalue
    Y = np.zeros(4)
    # S
    Y[0] = - (r * beta1 * X[0] * X[2]) / N - (r * beta2 * X[0] * X[1]) / N
    # E
    Y[1] = (r * beta1 * X[0] * X[2]) / N + (r * beta2 * X[0] * X[1]) / N - sigma * X[1]
    # I
    Y[2] = sigma * X[1] - gamma * X[2]
    # R
    Y[3] = gamma * X[2]
    return Y

T_range = np.arange(0, T+1)
Res = spi.odeint(SEIR, INI, T_range)
S_t = Res[:, 0]
E_t = Res[:, 1]
I_t = Res[:, 2]
R_t = Res[:, 3]


# second period，after 1.23
S_2 = S_t[T]
E_2 = E_t[T]
I_2 = I_t[T]
R_2 = R_t[T]

beta1 = 0.02#0.15747
beta2 = 0.021/3          # 0.78735
# r2 * beta2 = 2
sigma2 = 1/4
#gamma = 1/6.736
r2 = 0.1
T2 = 150-T

#ode
INI = [S_2, E_2, I_2, R_2]
def SEIR(inivalue, _):
    X = inivalue
    Y = np.zeros(4)
    # S
    Y[0] = - (r2 * beta1 * X[0] * X[2]) / N - (r2 * beta2 * X[0] * X[1]) / N
    # E
    Y[1] = (r2 * beta1 * X[0] * X[2]) / N + (r2 * beta2 * X[0] * X[1]) / N - sigma2 * X[1]
    # I
    Y[2] = sigma2 * X[1] - gamma * X[2]
    # R
    Y[3] = gamma * X[2]
    return Y

T_range = np.arange(0, T2+1)
Res = spi.odeint(SEIR, INI, T_range)
S_t2 = Res[:, 0]
E_t2 = Res[:, 1]
I_t2 = Res[:, 2]
R_t2 = Res[:, 3]

# Show date
plt.figure(figsize=(10, 6))
import pandas as pd
xs = pd.date_range(start='20191124', periods=T+1, freq='1D')    # 生成2020-02-11类型的日期数组（）
#print(xs)
xs2 = pd.date_range(start='20200206', periods=T2+1, freq='1D')

#plt.plot(S_t, color='blue', label='Susceptibles')#, marker='.')
plt.plot(xs, E_t, color='grey', label='Exposed', marker='.')
plt.plot(xs2, E_t2, color='grey', label='Exposed Prediction')
plt.plot(xs, I_t, color='red', label='Infected', marker='.')
plt.plot(xs2, I_t2, color='red', label='Infected Prediction')
plt.plot(xs, I_t + R_t, color='green', label='Infected + Removed', marker='.')
plt.plot(xs2, I_t2 + R_t2, color='green', label='Cumulative Infections Prediction')
#plt.plot(np.arange(0, T+1, 1), I_t + R_t, color='green', label='Removed')
#plt.plot(np.arange(T, T+T2+1, 1), I_t2 + R_t2, color='green', label='Infected2')
#plt.xlabel('Date')
plt.ylabel('Number')
plt.title('SEIR Prediction(Hubei Province, 1.23 Intervention)')
plt.legend()

xs3 = pd.date_range(start='20200123', periods=1, freq='1D')
#plt.plot(xs3, np.arange(1000, 2000, 1000))
plt.annotate(r'$1.23-Intervention$', xy=(xs3, -3000), xycoords='data', xytext=(-47, -30), textcoords='offset points',
             fontsize=10, arrowprops=dict(arrowstyle='->', connectionstyle='arc3, rad=0'))

xs4 = pd.date_range(start='20200210', periods=1, freq='1D')
plt.annotate(r'$2.10-Peak$', xy=(xs4, 24700), xycoords='data', xytext=(-25, -130), textcoords='offset points',
             fontsize=10, arrowprops=dict(arrowstyle='->', connectionstyle='arc3, rad=0'))

xs5 = pd.date_range(start='20200401', periods=1, freq='1D')
plt.annotate(r'$4.1-Epidemic-Scale:62188$', xy=(xs5, 62188), xycoords='data', xytext=(-75, -60), textcoords='offset points',
             fontsize=10, arrowprops=dict(arrowstyle='->', connectionstyle='arc3, rad=0'))

xs6 = pd.date_range(start='20200123', periods=1, freq='1D')
plt.annotate(r'$1.23-Exposed:5257$', xy=(xs6, 5257), xycoords='data', xytext=(-180, -3), textcoords='offset points',
             fontsize=10, arrowprops=dict(arrowstyle='->', connectionstyle='arc3, rad=0'))

xs7 = pd.date_range(start='20191124', periods=1, freq='1D')
plt.annotate(r'$2019.11.24-0-Case$', xy=(xs7, -3000), xycoords='data', xytext=(-56, -30), textcoords='offset points',
             fontsize=10, arrowprops=dict(arrowstyle='->', connectionstyle='arc3, rad=0'))

xs8 = pd.date_range(start='20200206', periods=1, freq='1D')
plt.annotate(r'$14days-Delay$', xy=(xs8, 41000), xycoords='data', xytext=(-130, -3), textcoords='offset points',
             fontsize=10, arrowprops=dict(arrowstyle='<->', connectionstyle='arc3, rad=0'))
#plt.text(30, 10, r'$This\ is\ the\ some\ text.\ \mu_j\ \sigma_i\ \alpha_t$')
plt.show()
