import numpy as np
import matplotlib.pyplot as plt

def simulate_mm1_queue(lam, mu, num_events=1000000):
    # 检查lam和mu的值是否在0到1之间
    assert 0 < lam <= 1 and 0 < mu <= 1, "lam and mu should be between 0 and 1."
    # 检查mu是否为0
    assert mu != 0, "mu should not be 0"
    # 计算p值，确保p不会出现0或NaN
    p = np.nan_to_num(lam / mu)
    
    # 初始化模拟参数
    # 计算数据包到达时间，采用几何分布生成随机数
    arrival_times = np.cumsum(np.random.geometric(p, size=num_events))
    # 计算服务时间，采用几何分布生成随机数
    service_times = np.random.geometric(1 - p, size=num_events)
    # 初始化离开时间
    departure_times = np.zeros(num_events)

    # 模拟队列
    # 初始化队列长度数组
    queue_lengths = np.zeros(num_events)
    queue_lengths[0] = 0
    # 遍历每一个事件，计算队列长度和离开时间
    for i in range(1, num_events):
        # 计算队列长度
        queue_lengths[i] = max(queue_lengths[i-1] + arrival_times[i-1] - departure_times[i-1], 0)
        # 计算离开时间
        departure_times[i] = arrival_times[i] + service_times[i] + queue_lengths[i]

    # 计算平均队列长度和延迟
    avg_queue_length = np.mean(queue_lengths)
    avg_delay = np.mean(queue_lengths / lam)

    return avg_delay

# MM1队列的参数
mu = 0.75
num_events = 1000000
lambdas = [0.2, 0.4, 0.5, 0.6, 0.65, 0.7, 0.72, 0.74, 0.745]

# 模拟不同到达率下的队列，并计算预期延迟
delays = []
for lam in lambdas:
    delay = simulate_mm1_queue(lam, mu, num_events=num_events)
    delays.append(delay)

# 绘制预期延迟和到达率的关系图
plt.plot(lambdas, delays)
plt.title("MM1队列的预期延迟 vs. 到达率")
plt.xlabel("到达率(lambda)")
plt.ylabel("预期延迟")

# 汉字字体，优先使用楷体，找不到则使用黑体
plt.rcParams['font.sans-serif'] = ['Kaitt', 'SimHei']
 
# 正常显示负号
plt.rcParams['axes.unicode_minus'] = False

# plt.show()

plt.savefig("mm1_queue_expected_delay_vs_arrival_rate.png")