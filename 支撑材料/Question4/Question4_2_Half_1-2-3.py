import itertools

# 定义参数
cases = [
    {'p1': 0.1, 'Cb1': 22, 'Cd1': 4, 'p2': 0.1, 'Cb2': 22, 'Cd2': 4, 'p3': 0.1, 'Cb3': 20, 'Cd3': 4, 'pf': 0.1, 'Ca': 6, 'Cdf': 6, 'Cl': 40, 'Ct': 6, 'S': 200}
]

N = 100
n = 98
results = []

# 遍历所有决策变量组合
for D1, D2,D3, Df, Dd, Dr1, Dr2, Dr3, Dr, Dc1, Dc2, Dc3 in itertools.product([0, 1], repeat=12):
    for case in cases:

        N1 = (D1 * (1 - case['p1']) * N + (1 - D1) * n)
        N2 = (D1 *N1 *(1-case['p1']) + (1-D1)*N1)
        PF = (1 - (1 - (1-case['p1']) * (1-case['p2']))) * (1-case['pf'])

        C_det = N2 *Df*case['Cdf']+\
            D1*(1-case['p1'])*N1*(case['Cd1']*Dc1*(1-D1)+case['Cd2']*Dc2*(1-D2)+case['Cd3']*Dc3*(1-D3))*(Df*Dd*case['pf']+(1-D1)*N1*Df*(1-PF))+\
            (case['Cd1']*Dr1*(1-D1)+case['Cd2']*Dr2*(1-D2)+case['Cd3']*Dr3*(1-D3))*(D1*(1-case['p1'])*N1*(1-Df)*Dr*case['pf']+(1-D1)*N1*(1-Df)*Dr*(1-PF))

        C_ass = D1*(1-case['p1'])*N1*(
            case['Ca'] + (Df*Dd*case['pf']*case['Ca']/2)*(1-Dc1)*(1-Dc2)*(1-Dc3) +
            (Df*Dd*case['pf']*case['Ca']/2)*(Dc1*(1-case['p1'])*(1-D1)+Dc2*(1-case['p2'])*(1-D2)+Dc3*(1-case['p3'])*(1-D3)) +
            (1-Df)*Dr*case['pf']*case['Ca']/2*(3-Dr1-Dr2-Dr3)+
            (1-Df)*Dr*case['pf']*case['Ca']/2*(Dr1*(1-D1)*(1-case['p1'])+Dr2*(1-D2)*(1-case['p2'])+Dr3*(1-D3)*(1-case['p3']))
        )+\
        (1 - D1) * N1 * (
                case['Ca'] + (Df * Dd * (1-PF) * case['Ca'] / 2) * (1 - Dc1)*(1 - Dc2)*(1 - Dc3) +
                (Df * Dd * (1-PF) * case['Ca'] / 2)*(Dc1 * (1 - case['p1']) * (1 - D1) + Dc2 * (1 - case['p2']) * (1 - D2) + Dc3 * (1 - case['p3']) * (1 - D3)) +
                (1 - Df) * Dr * (1-PF) * case['Ca'] / 2 * (3 - Dr1 - Dr2 - Dr3) +
                (1 - Df) * Dr * (1-PF) * case['Ca'] / 2 * (Dr1 * (1 - D1) * (1 - case['p1']) + Dr2 * (1 - D2) * (1 - case['p2']) + Dr3 * (1 - D3) * (1 - case['p3']))
        )
        C_dis = N1*(Dd+Dr)*case['Ct']*(D1*case['pf']*(1-case['p1'])+(1-D1)*(1-PF))

        C_exc = N1 * (1 - Df)*(case['Cl']+case['S'])*(D1 * (1-case['p1'])*case['pf']+(1-D1)*(1-PF))
        # 总成本
        C_total = C_det + C_ass + C_dis + C_exc

        results.append({
            'case': case,
            'D1': D1,
            'D2': D2,
            'D3': D3,
            'Df': Df,
            'Dd': Dd,
            'Dr1': Dr1,
            'Dr2': Dr2,
            'Dr3': Dr3,
            'Dr': Dr,
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
    print(f"Case {case_index}:")
    print(f"  Best {result['D1']}, {result['D2']}, {result['Df']}, {result['Dd']}, {result['Dr1']},{result['Dr2']},{result['Dr']},{result['Dc1']},{result['Dc2']}  Minimum C_total: {result['C_total']}")
