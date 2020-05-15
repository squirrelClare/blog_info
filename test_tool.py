# -*- coding: utf-8 -*-
# @Time    : 2020/5/15 16:56
# @Author  : 张聪聪
# @Email   : zcc136314853@163.com
# @File    : test_tool.py
# @Software: PyCharm
import unittest

from HTMLTestRunner.HTMLTestRunner import HTMLTestRunner

import numpy as np

from job9.tool import Tool


class TestTool(unittest.TestCase):

    def setUp(self) -> None:
        print("初始化动作")

    def tearDown(self) -> None:
        print("收尾动作")

    def test_sum(self):
        self.assertEqual(12, Tool.sum(8, 4))

    def test_max_value(self):
        self.assertNotEqual(13, Tool.max_value(np.array([1,3])))

    def test_show(self):
        Tool.show('hello')
        print("测试完毕")
if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestTool))
    # unittest.TextTestRunner(verbosity=2).run(suite)

    # 添加encoding='utf-8'防止出现乱码
    f = open('d:/HTMLReport2.html', 'w', encoding='utf-8')
    runner = HTMLTestRunner(stream=f,
                            title='tool.py的Tool测试报告',
                            verbosity=2)
    runner.run(suite)