import itertools

# 定义参数
cases = [
    {'p1': 0.1, 'Cb1': 2, 'Cd1': 1, 'p2': 0.1, 'Cb2': 8, 'Cd2': 1,'p3': 0.1, 'Cb3': 12, 'Cd3': 2, 'pf': 0.1, 'Ca': 8, 'Cdf': 4, 'Ct': 6}
]

N = 100
results = []

# 遍历所有决策变量组合
for D1, D2, Df, Dd, Dr1, D3, Dc1, Dc2, Dc3, in itertools.product([0, 1], repeat=9):
    for case in cases:

        N1 = (D1 * (1 - case['p1']) * N + (1 - D1) * N) + (D2 * (1 - case['p2']) * N + (1 - D2) * N)
        PF = (1 - (1 - (1-case['p1']) * (1-case['p2']))) * (1-case['pf'])

        # 计算各项成本
        C_buy = N * (case['Cb1'] + case['Cb2'])
        C_det = (N *
                 Df * case['Cdf'] *(D1 * case['Cd1'] + D2 * case['Cd2'] + D3 * case['Cd1']) +
                 (D1*(1-case['p1'])*case['pf']*(case['Cd1']*Dc1 * (1-D1) +case['Cd2']*Dc2 * (1-D2)+case['Cd3']*Dc3 * (1-D3)))+
                 ((1-D1)*(Df*(1-PF)*((case['Cd1']*Dc1*(1-D1))+(case['Cd1']*Dc1*(1-D1))+(case['Cd1']*Dc1*(1-D1)))))
                 )

        C_ass = (N1*case['Ca']+D1*(1-case['p1'])*N+(1-D1)*N)*(
            Df*Dd*(1-PF)*case['Ca']/2*(3-D1-D2-D3+Dc1*(1-case['p1'])*(1-D1)+Dc2*(1-case['p2'])*(1-D2)+Dc3*(1-case['p3'])*(1-D3))
        )
        C_dis = N * case['Ct'] * Dd * (
                D1*(1-case['p1'])*case['pf']+(1-D1)*(1-PF)
        )


        # 总成本
        C_total = C_buy + C_det + C_ass + C_dis

        results.append({
            'case': case,
            'D1': D1,
            'D2': D2,
            'D3': D3,
            'Df': Df,
            'Dd': Dd,
            'Dr1': Dr1,
            'Dc1': Dc1,
            'Dc2': Dc2,
            'Dc3': Dc3,
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
    print(f"Case 零配件4+5+6:")
    print(f"  Best {result['D1']}, {result['D2']}, {result['Df']}, {result['Dd']}, {result['Dr1']},{result['D3']},{result['Dc3']},{result['Dc1']},{result['Dc2']}  Minimum C_total: {result['C_total']}")
