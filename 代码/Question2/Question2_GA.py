import numpy as np
from deap import base, creator, tools, algorithms

# 定义遗传算法的基本参数
POPULATION_SIZE = 100  # 种群大小
P_CROSSOVER = 0.7      # 交叉概率
P_MUTATION = 0.01      # 变异概率
MAX_GENERATIONS = 50   # 最大迭代次数
HALL_OF_FAME_SIZE = 1  # 存储最优解的数量

# 定义问题的决策变量
DECISION_VARS = ['D1', 'D2', 'Df', 'Dd', 'Dr1', 'Dr2', 'Dr', 'Dc1', 'Dc2']

# 创建适配度和个体类
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

# 初始化工具箱
toolbox = base.Toolbox()
toolbox.register("attr_bool", np.random.choice, [0, 1], p=[0.5, 0.5])
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=len(DECISION_VARS))
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


def evaluate(individual, case):
    # 解包个体
    D1, D2, Df, Dd, Dr1, Dr2, Dr, Dc1, Dc2 = individual

    # 根据case获取参数值
    p1, Cb1, Cd1, p2, Cb2, Cd2, pf, Ca, Cdf, Cl, Ct, S = cases[case]

    # 计算公式
    N = 100
    N1 = (D1 * (1 - p1) * N + (1 - D1) * N) + (D2 * (1 - p2) * N + (1 - D2) * N)
    PF = (1 - (1 - (1 - p1) * (1 - p2))) * (1 - pf)

    C_buy = N * (Cb1 + Cb2)
    C_det = (N * (D1 * Cd1 + D2 * Cd2) + Df * Cdf * N1 +
             (pf * N * (D1 * (1 - p1) + D2 * (1 - p1)) + N * (1 - PF) * ((1 - D1) * (1 - D2))) *
             (Df * Dd * (Cd1 * (Dc1 + Dr1) * (1 - D1) + Cd2 * (Dc2 + Dr2) * (1 - D2))))

    C_ass = N1 * Ca + N * (D1 * (1 - p1) + D2 * (1 - p2)) * (
            Df * Dd * pf * Ca / 2 * (
                2 - Dc1 - Dc2 + Dc1 * (1 - p1) * (1 - D1) + Dc2 * (1 - p2) * (1 - D2)) +
            (1 - Df) * Dr * pf * Ca / 2 * (
                        2 - Dr1 - Dr2 + Dr1 * (1 - p1) * (1 - D1) + (1 - p2) * (1 - D2)) +
            N * (2 - D1 - D2) * (
                    Df * Dd * (1 - PF) * Ca / 2 * (
                        2 - Dc1 - Dc2 + Dc1 * (1 - p1) * (1 - D1) + Dc2 * (1 - p2) * (1 - D2)) +
                    (1 - Df) * Dr * Ca / 2 * (1 - PF) * (
                                2 - Dr1 - Dr2 + Dr1 * (1 - p1) * (1 - D1) + Dr2 * (1 - p2) * (1 - D2))
            )
    )
    C_dis = N * Ct * (Dd + Dr) * pf * (D1*(1-p1) + D2 * (1-p2)) + (1 - PF) * N * Ct * (Dd + Dr) * ((1-D1)+(1-D2))
    
    C_exc = N * pf * ((1-Df)*(Cl+S)) * (D1*(1-p1)+D1*(1-p1)) + N *(1-PF)*(1-Df)*(Cl+S)*(2-D1-D2)

    return C_buy + C_det + C_ass + C_dis + C_exc,


# 注册评估函数
toolbox.register("evaluate", evaluate, case=1)  # 初始设置为第一种情况

toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)

cases = [
    [0.1, 4, 2, 0.1, 18, 3, 0.1, 6, 3, 6, 5, 56],
    [0.2, 4, 2, 0.2, 18, 3, 0.2, 6, 3, 6, 5, 56],
    [0.1, 4, 2, 0.1, 18, 3, 0.1, 6, 3, 30, 5, 56],
    [0.2, 4, 1, 0.2, 18, 1, 0.2, 6, 2, 30, 5, 56],
    [0.1, 4, 8, 0.2, 18, 1, 0.1, 6, 2, 10, 5, 56],
    [0.05, 4, 2, 0.05, 18, 3, 0.05, 6, 3, 10, 40, 56]
]

for i, case in enumerate(cases):
    # 更新评估函数中的case参数
    toolbox.unregister("evaluate")
    toolbox.register("evaluate", evaluate, case=i)

    # 创建初始种群
    population = toolbox.population(n=POPULATION_SIZE)

    # 历史记录
    hof = tools.HallOfFame(HALL_OF_FAME_SIZE)

    # 运行遗传算法
    algorithms.eaSimple(population, toolbox, cxpb=P_CROSSOVER, mutpb=P_MUTATION,
                        ngen=MAX_GENERATIONS, halloffame=hof, verbose=False)

    print(f"Case {i + 1}: Best individual is {hof[0]} with cost {hof[0].fitness.values[0]}")
