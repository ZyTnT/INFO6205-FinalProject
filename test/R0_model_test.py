import unittest
from main.R0_model import R0Func
import configparser
import os

class TestR0_calculator(unittest.TestCase):

    conf = configparser.ConfigParser()
    curpath = os.path.dirname(os.path.realpath(__file__))
    cfgpath = os.path.join(curpath, "config.ini")
    conf.read(cfgpath, encoding="utf-8")

    confirm = int(conf['R0_calculator']['confirm'])
    susceptible = int(conf['R0_calculator']['susceptible'])
    t = int(conf['R0_calculator']['t'])

    def test_R0calculator_notNone(self):
        self.assertIsNotNone(R0Func(self.confirm, self.susceptible, self.t))

    def test_R0calculator_output1(self):
        self.assertAlmostEqual(1.36, round(R0Func(self.confirm, self.susceptible, self.t), 2))