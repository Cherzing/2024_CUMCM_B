import numpy as np
import matplotlib.pyplot as plt

# 设置matplotlib显示中文所需的字体
plt.rcParams['font.sans-serif'] = ['SimSun']  # 宋体
plt.rcParams['font.family'] = 'sans-serif'  # 使用sans-serif字体族
plt.rcParams['font.size'] = 17
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

# 定义参数
z = 1.645  # 拒收临界值
p = 0.11  # 抽样次品率

# 定义p0的两个范围
p0_range1 = np.linspace(0.05, 0.09, 500)  # p0的范围从0.05到0.09
p0_range2 = np.linspace(0.13, 0.15, 500)  # p0的范围从0.13到0.15

# 定义公式
n_range1 = (p0_range1 * (1 - p0_range1) * z**2) / ((p - p0_range1)**2)
n_range2 = (p0_range2 * (1 - p0_range2) * z**2) / ((p - p0_range2)**2)

# 绘制图形
plt.figure(figsize=(10, 6))
plt.plot(p0_range1, n_range1, label=r'$p_0 \in [0.05, 0.09]$')
plt.plot(p0_range2, n_range2, label=r'$p_0 \in [0.13, 0.15]$')
plt.xlabel('标称次品率 p0')
plt.ylabel('样本量 n')
plt.legend()
plt.grid(True)
plt.show()
