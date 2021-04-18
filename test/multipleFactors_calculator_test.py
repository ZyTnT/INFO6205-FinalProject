import unittest
from main.calculator import multiple_factors_calculator
import configparser
import os
import matplotlib.pyplot as plt

class TestMultipleFactors_calculator(unittest.TestCase):

    conf = configparser.ConfigParser()
    curpath = os.path.dirname(os.path.realpath(__file__))
    cfgpath = os.path.join(curpath, "config.ini")
    conf.read(cfgpath, encoding="utf-8")

    N = int(conf['mutiple_factors']['N'])
    S_0 = int(conf['mutiple_factors']['S_0'])
    E_0 = int(conf['mutiple_factors']['E_0'])
    I_0 = int(conf['mutiple_factors']['I_0'])
    recovery = int(conf['mutiple_factors']['recovery'])
    confirmTime = int(conf['mutiple_factors']['confirmTime'])
    latentTime = int(conf['mutiple_factors']['latentTime'])
    r = int(conf['mutiple_factors']['r'])
    T = int(conf['mutiple_factors']['T'])
    afterDays = int(conf['mutiple_factors']['afterDays'])
    methods = eval(conf['mutiple_factors']['methods'])

    def testMultipleFactorsCalculator_notNone(self):
        self.assertIsNotNone(multiple_factors_calculator(self.N, self.S_0, self.E_0, self.I_0, self.recovery, self.confirmTime, self.latentTime, self.r, self.T, self.afterDays, self.methods))

    def test_multipleFactorsCaculator_byGraph(self):
        S_t, E_t, I_t, R_t, reproductionList = multiple_factors_calculator(self.N, self.S_0, self.E_0, self.I_0, self.recovery, self.confirmTime, self.latentTime, self.r, self.T, self.afterDays, self.methods)
        plt.plot(S_t, color='blue', label='Susceptibles')  # , marker='.')
        plt.plot(E_t, color='grey', label='Exposed')
        plt.plot(I_t, color='red', label='Infected')
        plt.plot(R_t, color='green', label='Recoverd')
        plt.plot(reproductionList, color='yellow', label='Reproduction Number')
        plt.xlabel('Day')
        plt.ylabel('Number')
        plt.title('SEIR Model')
        plt.legend()
        plt.show()

