import random
import math

N = 100
n = 98

# 定义参数
cases = [
    {'p1': 0.1, 'Cb1': 4, 'Cd1': 2, 'p2': 0.1, 'Cb2': 18, 'Cd2': 3, 'pf': 0.1, 'Ca': 6, 'Cdf': 3, 'Cl': 6, 'Ct': 5, 'S': 56},
    {'p1': 0.2, 'Cb1': 4, 'Cd1': 2, 'p2': 0.2, 'Cb2': 18, 'Cd2': 3, 'pf': 0.2, 'Ca': 6, 'Cdf': 3, 'Cl': 6, 'Ct': 5, 'S': 56},
    {'p1': 0.1, 'Cb1': 4, 'Cd1': 2, 'p2': 0.1, 'Cb2': 18, 'Cd2': 3, 'pf': 0.1, 'Ca': 6, 'Cdf': 3, 'Cl': 30, 'Ct': 5, 'S': 56},
    {'p1': 0.2, 'Cb1': 4, 'Cd1': 1, 'p2': 0.2, 'Cb2': 18, 'Cd2': 1, 'pf': 0.2, 'Ca': 6, 'Cdf': 2, 'Cl': 30, 'Ct': 5, 'S': 56},
    {'p1': 0.1, 'Cb1': 4, 'Cd1': 8, 'p2': 0.2, 'Cb2': 18, 'Cd2': 1, 'pf': 0.1, 'Ca': 6, 'Cdf': 2, 'Cl': 10, 'Ct': 5, 'S': 56},
    {'p1': 0.05, 'Cb1': 4, 'Cd1': 2, 'p2': 0.05, 'Cb2': 18, 'Cd2': 3, 'pf': 0.05, 'Ca': 6, 'Cdf': 3, 'Cl': 10, 'Ct': 40, 'S': 56}
]


def calculate_cost(case, D1, D2, Df, Dd, Dr1, Dr2, Dr, Dc1, Dc2):
    N1 = (D1 * (1 - case['p1']) * n + (1 - D1) * n)
    PF = (1 - (1 - (1 - case['p1']) * (1 - case['p2']))) * (1 - case['pf'])

    # 计算各项成本
    C_buy = N * (case['Cb1'] + case['Cb2'])
    C_det = n * N1 * Df * case['Cdf'] + \
            (D1 * (1 - case['p1']) * N) * (
                        Df * Dd * case['pf'] * n * (case['Cd1'] * Dc1 * (1 - D1) + (case['Cd2'] * Dc2 * (1 - D2)))) + \
            D1 * (1 - case['p1']) * N * (1 - Df) * Dr * case['pf'] * (
                        case['Cd1'] * Dr1 * (1 - D1) + case['Cd2'] * Dr2 * (1 - D2)) * n + \
            (1 - D1) * N * (1 - Df) * Dr * (1 - PF) * (case['Cd1'] * (1 - D1) * Dr1 + case['Cd2'] * (1 - D2) * Dr2)

    C_ass = N1 * case['Ca'] + N * (D1 * (1 - case['p1']) + D2 * (1 - case['p2'])) * (
            Df * Dd * case['pf'] * case['Ca'] / 2 * (
                2 - Dc1 - Dc2 + Dc1 * (1 - case['p1']) * (1 - D1) + Dc2 * (1 - case['p2']) * (1 - D2)) +
            (1 - Df) * Dr * case['pf'] * case['Ca'] / 2 * (
                        2 - Dr1 - Dr2 + Dr1 * (1 - case['p1']) * (1 - D1) + (1 - case['p2']) * (1 - D2)) +
            N * (2 - D1 - D2) * (
                    Df * Dd * (1 - PF) * case['Ca'] / 2 * (
                        2 - Dc1 - Dc2 + Dc1 * (1 - case['p1']) * (1 - D1) + Dc2 * (1 - case['p2']) * (1 - D2)) +
                    (1 - Df) * Dr * case['Ca'] / 2 * (1 - PF) * (
                                2 - Dr1 - Dr2 + Dr1 * (1 - case['p1']) * (1 - D1) + Dr2 * (1 - case['p2']) * (1 - D2))
            )
    )
    C_dis = N * case['Ct'] * (Dd + Dr) * case['pf'] * (D1 * (1 - case['p1']) + D2 * (1 - case['p2'])) + (1 - PF) * N * \
            case['Ct'] * (Dd + Dr) * ((1 - D1) + (1 - D2))

    C_exc = N * case['pf'] * ((1 - Df) * (case['Cl'] + case['S'])) * (
                D1 * (1 - case['p1']) + D1 * (1 - case['p1'])) + N * (1 - PF) * (1 - Df) * (case['Cl'] + case['S']) * (
                        2 - D1 - D2)

    # 总成本
    C_total = C_buy + C_det + C_ass + C_dis + C_exc
    return C_total


def generate_initial_solution():
    return [random.choice([0, 1]) for _ in range(9)]


def get_neighbor(solution):
    new_solution = solution.copy()
    index_to_change = random.randint(0, len(new_solution) - 1)
    new_solution[index_to_change] = 1 - new_solution[index_to_change]
    return new_solution


def acceptance_probability(cost_diff, T):
    return math.exp(-cost_diff / T)


def simulated_annealing(case):
    current_solution = generate_initial_solution()
    current_cost = calculate_cost(case, *current_solution)

    T = 1000  # 初始温度
    alpha = 0.99  # 冷却率
    while T > 1e-5:
        for _ in range(100):  # 每个温度下的迭代次数
            new_solution = get_neighbor(current_solution)
            new_cost = calculate_cost(case, *new_solution)
            cost_diff = new_cost - current_cost
            if cost_diff < 0 or random.random() < acceptance_probability(cost_diff, T):
                current_solution = new_solution
                current_cost = new_cost
        T *= alpha

    return current_solution, current_cost


# 对每个案例应用模拟退火算法
best_results = {}
for case in cases:
    case_key = tuple(case.values())
    best_solution, best_cost = simulated_annealing(case)
    best_results[case_key] = {
        'D1': best_solution[0],
        'D2': best_solution[1],
        'Df': best_solution[2],
        'Dd': best_solution[3],
        'Dr1': best_solution[4],
        'Dr2': best_solution[5],
        'Dr': best_solution[6],
        'Dc1': best_solution[7],
        'Dc2': best_solution[8],
        'C_total': best_cost
    }

# 输出结果
for case_key, result in best_results.items():
    case_index = cases.index(dict(zip(cases[0].keys(), case_key))) + 1
    print(f"Case {case_index}:")
    print(
        f"  Best {result['D1']}, {result['D2']}, {result['Df']}, {result['Dd']}, {result['Dr1']},{result['Dr2']},{result['Dr']},{result['Dc1']},{result['Dc2']}  Minimum C_total: {result['C_total']}")
