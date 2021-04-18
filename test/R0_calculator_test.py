import unittest
from main.calculator import R0_calculator
import configparser
import os
import matplotlib.pyplot as plt

class TestR0_calculator(unittest.TestCase):

    conf = configparser.ConfigParser()
    curpath = os.path.dirname(os.path.realpath(__file__))
    cfgpath = os.path.join(curpath, "config.ini")
    conf.read(cfgpath, encoding="utf-8")

    N = int(conf['calculator']['N'])
    S_0 = int(conf['calculator']['S_0'])
    E_0 = int(conf['calculator']['E_0'])
    I_0 = int(conf['calculator']['I_0'])
    recovery = int(conf['calculator']['recovery'])
    R0 = int(conf['calculator']['R0'])
    T = int(conf['calculator']['T'])

    def test_R0calculator_notNone(self):
        self.assertIsNotNone(R0_calculator(self.N, self.S_0, self.E_0, self.I_0, self.recovery, self.R0, self.T))

    def test_R0caculator_byGraph(self):
        S_t, E_t, I_t, R_t = R0_calculator(self.N, self.S_0, self.E_0, self.I_0, self.recovery, self.R0, self.T)
        # reproductionList = np.array(reproductionList)
        plt.plot(S_t, color='blue', label='Susceptibles')  # , marker='.')
        plt.plot(E_t, color='grey', label='Exposed')
        plt.plot(I_t, color='red', label='Infected')
        plt.plot(R_t, color='green', label='Recoverd')
        # plt.plot(reproductionList, color='yellow', label='Reproduction Number')
        plt.xlabel('Day')
        plt.ylabel('Number')
        plt.title('SEIR Model')
        plt.legend()
        plt.show()
        print()

