import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


# 定义拟合函数
def func(x, a, b, c):
    return a + b / (x + c)


if __name__ == '__main__':
    # 读取CSV文件
    df = pd.read_csv('Data/map.csv')

    # 获取x和y数据列
    x_data = df['a_avg'].values
    y_data = df['m'].values

    # 使用curve_fit进行拟合
    popt, _ = curve_fit(func, x_data, y_data)

    # 提取拟合参数
    a_fit, b_fit, c_fit = popt

    print('para_a = ',a_fit)
    print('para_b = ',b_fit)
    print('para_c = ',c_fit)

    # 绘制原始数据和拟合曲线
    x_fit = np.linspace(min(x_data), max(x_data), 100)
    y_fit = func(x_fit, a_fit, b_fit, c_fit)

    plt.plot(x_data, y_data, 'bo', label='origin')
    plt.plot(x_fit, y_fit, 'r-', label='fit')
    plt.legend()
    plt.xlabel('a')
    plt.ylabel('m')
    plt.show()
