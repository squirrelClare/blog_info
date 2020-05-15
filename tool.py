# -*- coding: utf-8 -*-
# @Time    : 2020/5/15 16:41
# @Author  : 张聪聪
# @Email   : zcc136314853@163.com
# @File    : tool.py
# @Software: PyCharm
import numpy as np

class Tool(object):
    @staticmethod
    def sum(a, b):
        return a + b;

    @staticmethod
    def max_value(array):
        return np.max(array)

    @staticmethod
    def show(value):
        print(value)
