import itertools

# 定义参数
cases = [
    {'p1': 0.1, 'Cb1': 4, 'Cd1': 2, 'p2': 0.1, 'Cb2': 18, 'Cd2': 3, 'pf': 0.1, 'Ca': 6, 'Cdf': 3, 'Cl': 6, 'Ct': 5, 'S': 56}
]

N = 10
results = []

# 遍历所有决策变量组合
for D1, D2, Df, Dd, Dr1, Dr2, Dr, Dc1, Dc2 in itertools.product([0, 1], repeat=9):
    for case in cases:
        # 计算 Q1 和 Q2
        Q1 = max(1, int(N / ((1 - case['p1']) * (1 - case['pf']))))
        Q2 = max(1, int(N / ((1 - case['p2']) * (1 - case['pf']))))

        # 计算各项成本
        C_buy = N * (case['Cb1']+ case['Cb2'])
        C_det = N * (
            D1 * (case['Cd1']) + D2 * (case['Cd2']) +
            Df * case['Cdf'] +
            Df * Dd * case['pf'] * (case['Cd1'] * Dc1 * (1 - D1) + case['Cd2'] * Dc2 * (1 - D2)) +
            (1 - Df) * Dr * case['pf'] * (
                    case['Cd1'] * (1 - D1) * Dr1 + case['Cd2'] * (1 - D2) * Dr2
            )
        )
        C_ass = N * (
            case['Ca'] +
            Df * Dd * (1 - (1 - case['p1']) * (1 - case['p2'])) * (
                (1 - Dc1) * (case['Ca'] / 2) +
                (1 - Dc2) * (case['Ca'] / 2) +
                Dc1 * (1 - case['p1']) * (case['Ca'] / 2) * (1 - D1) +
                Dc2 * (1 - case['p2']) * (case['Ca'] / 2) * (1 - D2)
            ) +
            (1 - Df) * Dr * (1 - (1 - case['p1']) * (1 - case['p2'])) * (
                (1 - Dr1) * (case['Ca'] / 2) +
                (1 - Dr2) * (case['Ca'] / 2) +
                Dr1 * (1 - case['p1']) * (case['Ca'] / 2) * (1 - D1) +
                Dr2 * (1 - case['p2']) * (case['Ca'] / 2) * (1 - D2)
            )
        )
        C_dis = N * (Dd * case['pf'] * case['Ct'] + Dr1 * case['pf'] * case['Ct'] + Dr2 * case['pf'] * case['Ct'])
        C_exc = N * ((1 - Df) * case['pf'] * (case['Cl'] + case['S']))

        # 总成本
        C_total = C_buy + C_det + C_ass + C_dis + C_exc

        results.append({
            'case': case,
            'D1': D1,
            'D2': D2,
            'Df': Df,
            'Dd': Dd,
            'Dr1': Dr1,
            'Dr2': Dr2,
            'Dr': Dr,
            'Dc1': Dc1,
            'Dc2': Dc2,
            'Q1': Q1,
            'Q2': Q2,
            'C_total': C_total
        })

# 找到每种情况下的最小成本及其对应的决策变量
best_results = {}
for case in cases:
    # 使用元组作为键
    case_key = tuple(case.values())
    best_result = min([r for r in results if tuple(r['case'].values()) == case_key], key=lambda x: x['C_total'])
    best_results[case_key] = best_result

# 输出结果
for case_key, result in best_results.items():
    case_index = cases.index(dict(zip(cases[0].keys(), case_key))) + 1
    print(f"Case {case_index}:")
    print(f"  Best D1: {result['D1']}, D2: {result['D2']}, Df: {result['Df']}, Dd: {result['Dd']}, Dr1: {result['Dr1']}, Dr2: {result['Dr2']}, Dr: {result['Dr']}, Dc1: {result['Dc1']}, Dc2: {result['Dc2']}")
    print(f"  Best Q1: {result['Q1']}, Q2: {result['Q2']}")
    print(f"  Minimum C_total: {result['C_total']}\n")
