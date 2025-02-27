import unittest

import matplotlib.pyplot as plt
import numpy as np

from src.cjlutils import PyplotUtil
from src.cjlutils.PyplotUtil import GraphType


class SimpleDrawCase(unittest.TestCase):

    def test_scatter(self):
        x: np.ndarray = np.array(list(range(-10, 11)))
        y = x ** 2

        # 创建一个图形并绘制点图
        figure_index = 1
        title = '点图 Scatter Plot'
        PyplotUtil.simple_draw(x, y, figure_order=figure_index, graph_type=GraphType.SCATTER, show=True, label='line',
                               title=title, save_path=f'./img/{title}.png')

    def test_many_scatters(self):
        repeat = 10
        title = '点图 Scatters Plot'
        figure_index = 1
        for i in range(repeat):
            # 创建一个图形并绘制点图
            x: np.ndarray = np.array(list(range(-i, i + 1)))
            y = x + i
            PyplotUtil.simple_draw(x, y, figure_order=figure_index, graph_type=GraphType.SCATTER, show=False,
                                   title=title, label=f'line {i}', save_path=f'./img/{title}.png')
        plt.show()

    def test_line(self):
        x: np.ndarray = np.array(list(range(-10, 11)))
        y = x ** 2

        # 创建一个图形并绘制折线图
        figure_index = 1
        title = '折线图 Line Plot'
        PyplotUtil.simple_draw(x, y, figure_order=figure_index, graph_type=GraphType.LINE, show=True, title=title,
                               label='line', save_path=f'./img/{title}.png')

    def test_many_lines(self):
        repeat = 10
        title = '折线图 Lines Plot'
        figure_index = 1
        for i in range(repeat):
            # 创建一个图形并绘制点图
            x: np.ndarray = np.array(list(range(-10, 11)))
            y = x ** 2 - i * x
            PyplotUtil.simple_draw(x, y, figure_order=figure_index, graph_type=GraphType.LINE, show=False,
                                   title=title, label=f'line {i}', save_path=f'./img/{title}.png')
        plt.title(title)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.show()

    def test_bar(self):
        x: np.ndarray = np.array(list(range(-10, 11)))
        y = x ** 2

        # 创建一个图形并绘制柱状图
        figure_index = 1
        title = '柱状图 Bar Plot'
        PyplotUtil.simple_draw(x, y, figure_order=figure_index, graph_type=GraphType.BAR, show=True, title=title,
                               label='line', save_path=f'./img/{title}.png')

    def test_pie(self):
        x: np.ndarray = np.array(list(range(-10, 11)))
        y = x ** 2

        # 创建一个图形并绘制饼图
        figure_index = 1
        title = '饼图 Pie Plot'
        PyplotUtil.simple_draw(x, y, figure_order=figure_index, graph_type=GraphType.PIE, show=True, title=title,
                               label='line', save_path=f'./img/{title}.png')

    def test_hist(self):
        x: np.ndarray = np.array(list(range(-10, 11)))
        y = x ** 2

        # 创建一个图形并绘制饼图
        figure_index = 1
        title = '直方图 Hist Plot'
        PyplotUtil.simple_draw(x, y, figure_order=figure_index, graph_type=GraphType.HIST, show=True, title=title,
                               label='line', save_path=f'./img/{title}.png')


if __name__ == '__main__':
    unittest.main()
