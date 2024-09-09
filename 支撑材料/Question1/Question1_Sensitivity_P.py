import numpy as np
import matplotlib.pyplot as plt

# 设置matplotlib显示中文所需的字体
plt.rcParams['font.sans-serif'] = ['SimSun']  # 宋体
plt.rcParams['font.family'] = 'sans-serif'  # 使用sans-serif字体族
plt.rcParams['font.size'] = 17
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

# 定义参数
p0 = 0.10  # 标称次品率
z = 1.645  # 拒收临界值

# 避免p等于p0的情况
p1 = np.linspace(0, 0.05, 500)  # p的范围从0到0.09（不包括0.1）
p2 = np.linspace(0.15, 0.3, 500)  # p的范围从0.11到0.3（不包括0.1）

# 重新定义公式
n1 = (p0 * (1 - p0) * z**2) / ((p1 - p0)**2)
n2 = (p0 * (1 - p0) * z**2) / ((p2 - p0)**2)

# 重新绘制图形
plt.figure(figsize=(10, 6))
plt.plot(p1, n1, label=r'$p \in [0, 0.05)$')
plt.plot(p2, n2, label=r'$p \in (0.15, 0.3]$')
plt.xlabel('次品率 p')
plt.ylabel('样本量 n')
plt.legend()
plt.grid(True)
plt.show()
