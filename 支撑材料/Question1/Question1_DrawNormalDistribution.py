import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm


# 设置matplotlib显示中文所需的字体
plt.rcParams['font.sans-serif'] = ['SimSun']  # 宋体
plt.rcParams['font.family'] = 'sans-serif'  # 使用sans-serif字体族
plt.rcParams['font.size'] = 17
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题


# 创建一个数值范围，从 -3.5 到 3.5，步长为 0.1
x = np.arange(-3.5, 3.5, 0.1)

# 计算这些数值对应的正态分布概率密度
y = norm.pdf(x)

# 绘制标准正态分布曲线
plt.figure(figsize=(10, 6))
plt.plot(x, y, label="标准正态分布")
plt.fill_between(x, y, alpha=0.2)
plt.xlabel("z-score")
plt.ylabel("概率密度")
plt.legend()
plt.grid(True)
plt.show()


# 创建一个数值范围，从 -3.5 到 3.5，步长为 0.1
x = np.arange(-3.5, 3.5, 0.1)

# 计算这些数值对应的正态分布累积概率
y = norm.cdf(x)

# 找到累积概率为90%和95%的z值
z_90 = norm.ppf(0.90)
z_95 = norm.ppf(0.95)

# 绘制标准正态分布累积概率曲线
plt.figure(figsize=(10, 6))
plt.plot(x, y, label="标准正态密度分布")
plt.xlabel("z-score")
plt.ylabel("累积概率")

# 标记累积概率为90%和95%的点
plt.plot(z_90, 0.90, 'ro')  # 红色点表示90%
plt.plot(z_95, 0.95, 'bo')  # 蓝色点表示95%
plt.text(z_90, 0.90, f' (z={z_90:.3f},P=0.90)', verticalalignment='bottom', horizontalalignment='right')
plt.text(z_95, 0.95, f' (z={z_95:.3f},P=0.95)', verticalalignment='bottom', horizontalalignment='right')

plt.legend()
plt.grid(True)
plt.show()


"""
以下求出具体的值
"""
# 给定的累积概率
cumulative_probability_1 = 0.1
cumulative_probability_2 = 0.95

# 灵敏度分析
cumulative_probability_3 = 0.90
cumulative_probability_4 = 0.99
z_value3 = norm.ppf(cumulative_probability_3)
z_value4 = norm.ppf(cumulative_probability_4)

# 使用ppf函数（百分点函数）来找到对应的z值
z_value1 = norm.ppf(cumulative_probability_1)
z_value2 = norm.ppf(cumulative_probability_2)

print(z_value1, z_value2, z_value3, z_value4)