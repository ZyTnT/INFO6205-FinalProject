import unittest
from main.SEIR_model import SEIR
import configparser
import os


class TestMultipleFactors(unittest.TestCase):

    conf = configparser.ConfigParser()
    curpath = os.path.dirname(os.path.realpath(__file__))
    cfgpath = os.path.join(curpath, "config.ini")
    conf.read(cfgpath, encoding="utf-8")

    N = int(conf['mutiple_factors']['N'])
    S_0 = int(conf['mutiple_factors']['S_0'])
    E_0 = int(conf['mutiple_factors']['E_0'])
    I_0 = int(conf['mutiple_factors']['I_0'])
    recovery = int(conf['mutiple_factors']['recovery'])
    beta1 = float(conf['mutiple_factors']['beta1'])
    beta2 = float(conf['mutiple_factors']['beta2'])
    sigma = float(conf['mutiple_factors']['sigma'])
    gamma = float(conf['mutiple_factors']['gamma'])
    r = int(conf['mutiple_factors']['r'])

    inivalue = [S_0, E_0, I_0, recovery]

    def test_SEIR_notNone(self):
        self.assertIsNotNone(SEIR(self.inivalue, self.r, self.beta1, self.beta2, self.N, self.sigma, self.gamma),
                             msg='None')

    def test_SEIR_S(self):
        self.assertEqual(-11, SEIR(self.inivalue, self.r, self.beta1, self.beta2, self.N, self.sigma, self.gamma)[0], msg='Not Equal')

    def test_SEIR_E(self):
        self.assertEqual(8.9, SEIR(self.inivalue, self.r, self.beta1, self.beta2, self.N, self.sigma, self.gamma)[1], msg='Not Equal')

    def test_SEIR_I(self):
        self.assertEqual(1.1, SEIR(self.inivalue, self.r, self.beta1, self.beta2, self.N, self.sigma, self.gamma)[2], msg='Not Equal')

    def test_SEIR_R(self):
        self.assertEqual(1, SEIR(self.inivalue, self.r, self.beta1, self.beta2, self.N, self.sigma, self.gamma)[3], msg='Not Equal')
