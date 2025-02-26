import numpy as np

import matplotlib.pyplot as plt
from matplotlib import collections


def _mockXY():
    np.random.seed(42)
    m = 100
    X = 2 * np.random.rand(m)
    Y = 4 + 3 * X + np.random.randn(m)
    return X, Y


def _getColors(num):
    return list(map(lambda x: tuple([0.2 + x / num * 0.8, 0, 0]), range(num)))


def _getLines(theta0, theta1, x_start, x_end):
    y1 = []
    y2 = []
    points = []
    # 是原生python数组，只能用这种方式！！
    for i in range(len(theta0)):
        y1.append(theta0[i] + x_start * theta1[i])
        y2.append(theta0[i] + x_end * theta1[i])
    for i in range(len(theta0)):
        points.append([tuple([x_start, y1[i]]), tuple([x_end, y2[i]])])
    return points


def bgd(X, Y, **kwargs):
    alpha = kwargs.get("alpha", 0.1)
    # 从y=0开始出发
    theta0 = 0
    theta1 = 0
    THETA0 = []
    THETA1 = []
    # 随意数据
    tmp0 = 1.0
    tmp1 = 1.0
    cnt = 0
    deviation = kwargs.get("deviation", 1e-6)
    while abs(tmp0) > deviation and abs(tmp1) > deviation:
        tmp0 = 1 / len(X) * np.sum(theta0 + theta1 * X - Y)
        tmp1 = 1 / len(Y) * np.sum((theta0 + theta1 * X - Y) * X)
        theta0 = theta0 - alpha * tmp0
        theta1 = theta1 - alpha * tmp1
        THETA0.append(float(theta0))
        THETA1.append(float(theta1))
        cnt += 1
        print("第", cnt, "次迭代，系数分别为", theta0, theta1)
    print("最终结果为：", theta0, theta1)
    return THETA0, THETA1


def example_bgd():
    X, Y = _mockXY()
    bgd(X, Y)


def plot_bgd(X, Y, axis, **kwargs):
    # 获取参数
    theta0, theta1 = bgd(X, Y, **kwargs)
    lines = _getLines(theta0, theta1, axis[0], axis[1])
    fig, axes = plt.subplots(1, 1)
    axes.add_collection(
        collections.LineCollection(lines, colors=_getColors(len(lines)))
    )

    plt.plot(X, Y, "b.")
    plt.xlabel("x")
    plt.ylabel("y", rotation=0)
    plt.axis(axis)
    plt.show()


def example_plot_bgd():
    X, Y = _mockXY()
    plot_bgd(X, Y, [0, 2, 0, 15], alpha=0.1, deviation=1e-6)


if __name__ == "__main__":
    # example_bgd()
    example_plot_bgd()
