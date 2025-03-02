import random
import time


def rand_int_in_time_range(min_val, max_val, time_window_seconds):
    """
    在给定的最小值和最大值之间生成随机数，并且保证在特定时间窗口内生成的随机数相同。

    参数:
    min_val (int或float): 随机数范围的最小值。
    max_val (int或float): 随机数范围的最大值。
    time_window_seconds (int): 时间窗口的秒数，在这个时间窗口内生成的随机数保持一致。

    返回:
    int或float: 生成的随机数
    """
    current_time = int(time.time())
    # 计算当前时间所在的时间窗口起始时间戳
    window_start_time = current_time - (current_time % time_window_seconds)
    random.seed(window_start_time)
    return int(random.uniform(min_val, max_val))


if __name__ == '__main__':
    i = 0
    while i < 10:
        i += 1
        print(rand_int_in_time_range(0, 100, 2))
        time.sleep(0.5)
