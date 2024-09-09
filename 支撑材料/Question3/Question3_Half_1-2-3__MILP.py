import pulp

N = 1000

# 定义参数列表
cases = [
    {'p1': 0.1, 'Cb1': 4, 'Cd1': 2, 'p2': 0.1, 'Cb2': 18, 'Cd2': 3, 'pf': 0.1, 'Ca': 6, 'Cdf': 3, 'Cl': 6, 'Ct': 5, 'S': 56},
    {'p1': 0.2, 'Cb1': 4, 'Cd1': 2, 'p2': 0.2, 'Cb2': 18, 'Cd2': 3, 'pf': 0.2, 'Ca': 6, 'Cdf': 3, 'Cl': 6, 'Ct': 5, 'S': 56},
    {'p1': 0.1, 'Cb1': 4, 'Cd1': 2, 'p2': 0.1, 'Cb2': 18, 'Cd2': 3, 'pf': 0.1, 'Ca': 6, 'Cdf': 3, 'Cl': 30, 'Ct': 5, 'S': 56},
    {'p1': 0.2, 'Cb1': 4, 'Cd1': 1, 'p2': 0.2, 'Cb2': 18, 'Cd2': 1, 'pf': 0.2, 'Ca': 6, 'Cdf': 2, 'Cl': 30, 'Ct': 5, 'S': 56},
    {'p1': 0.1, 'Cb1': 4, 'Cd1': 8, 'p2': 0.2, 'Cb2': 18, 'Cd2': 1, 'pf': 0.1, 'Ca': 6, 'Cdf': 2, 'Cl': 10, 'Ct': 5, 'S': 56},
    {'p1': 0.05, 'Cb1': 4, 'Cd1': 2, 'p2': 0.05, 'Cb2': 18, 'Cd2': 3, 'pf': 0.05, 'Ca': 6, 'Cdf': 3, 'Cl': 10, 'Ct': 40, 'S': 56}
]

# 初始化结果列表
results = []

# 遍历每种情况
for case in cases:
    # 创建一个最小化问题
    prob = pulp.LpProblem("CostMinimization", pulp.LpMinimize)

    # 定义决策变量
    D1 = pulp.LpVariable('D1', cat='Binary')
    D2 = pulp.LpVariable('D2', cat='Binary')
    Df = pulp.LpVariable('Df', cat='Binary')
    Dd = pulp.LpVariable('Dd', cat='Binary')
    Dr1 = pulp.LpVariable('Dr1', cat='Binary')
    Dr2 = pulp.LpVariable('Dr2', cat='Binary')
    Dr = pulp.LpVariable('Dr', cat='Binary')
    Dc1 = pulp.LpVariable('Dc1', cat='Binary')
    Dc2 = pulp.LpVariable('Dc2', cat='Binary')

    # 计算 Q1 和 Q2
    Q1 = pulp.LpVariable('Q1', lowBound=int(N / ((1 - case['p1']) * (1 - case['pf']))), cat='Integer')
    Q2 = pulp.LpVariable('Q2', lowBound=int(N / ((1 - case['p2']) * (1 - case['pf']))), cat='Integer')

    # 定义目标函数
    C_buy = N * (case['Cb1'] * Q1 + case['Cb2'] * Q2)

    C_det = N * (
        D1 * (case['Cd1'] / (1 - case['p1'])) +
        D2 * (case['Cd2'] / (1 - case['p2'])) +
        Df * case['Cdf'] +
        Dd * case['pf'] * (
            case['Cd1'] * Dc1 * (1 - D1) +
            case['Cd2'] * Dc2 * (1 - D2)
        ) +
        Dr1 * case['pf'] * (case['Cd1'] * (1 - D1)) +
        Dr2 * case['pf'] * (case['Cd2'] * (1 - D2))
    )

    C_ass = N * (
        case['Ca'] +
        Dd * (1 - (1 - case['p1']) * (1 - case['p2'])) * (
            (1 - Dc1) * (case['Ca'] / 2) +
            (1 - Dc2) * (case['Ca'] / 2) +
            Dc1 * (1 - case['p1']) * (case['Ca'] / 2) * (1 - D1) +
            Dc2 * (1 - case['p2']) * (case['Ca'] / 2) * (1 - D2)
        ) +
        Dr * (1 - (1 - case['p1']) * (1 - case['p2'])) * (
            (1 - Dr1) * (case['Ca'] / 2) +
            (1 - Dr2) * (case['Ca'] / 2) +
            Dr1 * (1 - case['p1']) * (case['Ca'] / 2) * (1 - D1) +
            Dr2 * (1 - case['p2']) * (case['Ca'] / 2) * (1 - D2)
        )
    )

    C_dis = N * (Dd * case['pf'] * case['Ct'] + Dr1 * case['pf'] * case['Ct'] + Dr2 * case['pf'] * case['Ct'])

    C_exc = N * ((1 - Df) * case['pf'] * (case['Cl'] + case['S']))

    prob += C_buy + C_det + C_ass + C_dis + C_exc, "TotalCost"

    # 解决问题
    prob.solve()

    # 存储结果
    result = {
        'D1': D1.varValue,
        'D2': D2.varValue,
        'Df': Df.varValue,
        'Dd': Dd.varValue,
        'Dr1': Dr1.varValue,
        'Dr2': Dr2.varValue,
        'Dr': Dr.varValue,
        'Dc1': Dc1.varValue,
        'Dc2': Dc2.varValue,
        'Q1': Q1.varValue,
        'Q2': Q2.varValue,
        'C_total': pulp.value(prob.objective)
    }

    results.append(result)

# 输出结果
for i, result in enumerate(results):
    print(f"Case {i + 1}: {result}")
