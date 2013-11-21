__author__ = 'maciejbanasiewicz'
from pprint import pprint
import sys
import math
import random
import numpy as np
import string
import copy
from array import array

class ProblemAbstract:
    '''
    Abstract class for all optimalization problems
    '''
    def value(self, vector=[]):
        pass
    def g(self, vector=[]):
        pass
    def array_value(self,array_of_vectors):
        ret = []
        for vector in array_of_vectors:
            ret.append(self.value(vector))
        return ret

class ZDT2(ProblemAbstract):
    """
    xi - [0, 1]
    i - [1, 5]
    """
    def value(self, vector=[]):
        g_value = self.g(vector)
        f_one = vector[0]
        f_two = g_value * (1 - ((f_one / g_value) ** 2))
        return [f_one, f_two]

    def g(self, vector=[]):
        # aka 'n'
        vector_len = len(vector)
        vector_sum = sum(vector[1:])
        return 1 + 9 * (vector_sum / (vector_len - 1))

class ZDT3(ProblemAbstract):
    """
    xi - [0, 1]
    i - [1, 10]
    """
    def value(self, vector=[]):
        g_value = self.g(vector)
        f_one = vector[0]
        f_two = g_value * ( 1 - ( (f_one / g_value) ** 0.5 ) - (f_one / g_value) * math.sin(10*math.pi * f_one))
        return [f_one, f_two]

    def g(self, vector=[]):
        # aka 'n'
        vector_len = len(vector)
        vector_sum = sum(vector[1:])
        return 1 + 9 * (vector_sum / (vector_len - 1))

class ZDT6(ProblemAbstract):
    """
    xi - [0, 1]
    i - [1, 5]
    """

    def value(self, vector=[]):
        g_value = self.g(vector)
        x1 = vector[0]
        f_one = 1 - math.exp(-4 * x1) * math.sin(4*math.pi * x1)**6
        f_two = g_value * ( 1 - ( f_one / g_value ) ** 2 )
        return [f_one, f_two]

    def g(self, vector=[]):
        # aka 'n'
        vector_len = len(vector)
        vector_sum = sum(vector[1:])
        return 1 + 9 * ( (vector_sum / (vector_len - 1)) ** 0.25 )