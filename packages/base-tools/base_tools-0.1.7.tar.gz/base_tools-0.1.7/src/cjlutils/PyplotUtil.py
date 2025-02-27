from enum import Enum
from typing import Sequence

import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')


class GraphType(Enum):
    # 散点图
    SCATTER = 0, 'scatter',
    # 折线图
    LINE = 1, 'line',
    # 柱状图
    BAR = 2, 'bar'
    # 饼图
    PIE = 3, 'pie'
    # 直方图
    HIST = 4, 'hist'


def simple_draw(xs: Sequence, ys: Sequence, figure_order: int = 0,
                graph_type: GraphType = GraphType.SCATTER, show: bool = True, title: str = None,
                label: str | Sequence[str] | None = None,
                xlabel: str = None, ylabel: str = None, save_path: str = None, drawer_size: int = 1) -> bool:
    """
    绘制简单的图形，支持折线图、散点图、柱状图、饼图、直方图、箱线图

    :param xs: x轴数据，与y轴数据长度相同，用于绘制图形
    :param ys: y轴数据，与x轴数据长度相同，用于绘制图形
    :param figure_order: 背景板标号
    :param graph_type: 图形类型
    :param show: 是否展示图形
    :param title: 标题栏文字
    :param label: 图例
    :param xlabel: x坐标轴文字
    :param ylabel: y坐标轴文字
    :param save_path: 保存图片的路径
    :param drawer_size: 笔尖大小
    :return:
    """
    plt.figure(figure_order)
    if graph_type == GraphType.LINE:
        plt.plot(xs, ys, label=label, linewidth=drawer_size)
    elif graph_type == GraphType.SCATTER:
        plt.scatter(xs, ys, label=label, s=drawer_size)
    elif graph_type == GraphType.BAR:
        plt.bar(xs, ys, label=label, width=drawer_size)
    elif graph_type == GraphType.PIE:
        plt.pie(ys, labels=xs, autopct='%1.1f%%')
    elif graph_type == GraphType.HIST:
        plt.hist(ys, bins=xs, label=label, rwidth=drawer_size)
    else:
        return False
    if label is not None:
        plt.legend()
    if title is not None:
        plt.title(title)
    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)
    if save_path is not None:
        plt.savefig(save_path)
    if show:
        plt.show(block=True)
    return True
