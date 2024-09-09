import numpy as np
import matplotlib.pyplot as plt

# 设置matplotlib显示中文所需的字体
plt.rcParams['font.sans-serif'] = ['SimSun']  # 宋体
plt.rcParams['font.family'] = 'sans-serif'  # 使用sans-serif字体族
plt.rcParams['font.size'] = 17
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

# 定义参数
p0 = 0.10  # 标称次品率
d = 0.05   # 检测误差

# 定义z的取值范围
z = np.linspace(1.282, 2.326, 400)

# 计算n的值
n = p0 * (1 - p0) * z**2 / d**2

# 绘制n随z变化的曲线
plt.figure(figsize=(10, 6))
plt.plot(z, n, label=r'$n=\frac{p_0(1-p_0)z^2}{d^2}$')
plt.xlabel('z值')
plt.ylabel('样本量 n')
plt.legend()
plt.grid(True)
plt.show()
