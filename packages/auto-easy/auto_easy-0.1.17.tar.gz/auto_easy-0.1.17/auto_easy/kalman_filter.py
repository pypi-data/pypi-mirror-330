import time

import numpy as np

from auto_easy.models import YoloItem, Point
from auto_easy.utils import logger


# 卡尔曼滤波器
class KalmanFilter:
    def __init__(self, process_variance=1e-2, measurement_variance=1e-1):
        # 状态向量: [x, y, v_x, v_y] 位置和速度
        self.x = np.zeros(4)  # 初始状态为 [x=0, y=0, v_x=0, v_y=0]

        # 状态转移矩阵 A
        self.A = np.array([[1, 0, 1, 0],  # x -> x + v_x * dt
                           [0, 1, 0, 1],  # y -> y + v_y * dt
                           [0, 0, 1, 0],  # v_x -> v_x (匀速运动假设)
                           [0, 0, 0, 1]])  # v_y -> v_y (匀速运动假设)

        # 观测矩阵 H
        self.H = np.array([[1, 0, 0, 0],  # 直接观测 x
                           [0, 1, 0, 0]])  # 直接观测 y

        # 过程噪声协方差矩阵 Q
        self.Q = np.eye(4) * process_variance

        # 观测噪声协方差矩阵 R
        self.R = np.eye(2) * measurement_variance

        # 初始估计协方差矩阵 P
        self.P = np.eye(4) * 1.0
        self.prev_time = time.time()

    def predict(self, dt):
        """
        根据时间间隔 dt 预测下一个位置
        """
        # dt = t - self.prev_time
        # self.prev_time = t
        # 更新状态转移矩阵 A, 使得它与 dt 相关
        self.A[0, 2] = dt  # x 方向上，位置变化与速度 * 时间步长成正比
        self.A[1, 3] = dt  # y 方向上，位置变化与速度 * 时间步长成正比

        # 预测步骤：使用状态转移矩阵 A 更新状态
        self.x = np.dot(self.A, self.x)
        self.P = np.dot(np.dot(self.A, self.P), self.A.T) + self.Q  # 更新协方差

    def update(self, z):
        """
        更新步骤，z 是观测值 (x, y)
        """
        # 计算观测残差
        y = z - np.dot(self.H, self.x)

        # 计算卡尔曼增益
        S = np.dot(np.dot(self.H, self.P), self.H.T) + self.R
        K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))

        # 更新状态估计
        self.x = self.x + np.dot(K, y)

        # 更新协方差矩阵
        self.P = self.P - np.dot(np.dot(K, self.H), self.P)

    def get_state(self):
        """
        返回当前估计的状态（位置和速度）
        """
        return self.x[:2]  # 返回位置 [x, y]


# 卡尔曼滤波器封装
class SimpleKalmanFilter:
    def __init__(self):
        self.kf = KalmanFilter()
        self.prev_time = -1
        self.prev_point = None
        self.prev_extra = None

    def gen_dt(self, t):
        if self.prev_time == -1:
            dt = 0
        else:
            dt = t - self.prev_time
        self.prev_time = t
        return dt

    def add_data(self, t, point, extra=None):
        dt = self.gen_dt(t)

        # print(f'add data({id(self)}): {dt}, {point}')
        self.prev_point = point
        self.prev_extra = extra

        # 即便在有新的观测数据时，我们仍然需要先通过 predict() 计算出预测的状态，然后再用实际的观测数据来 校正 这个预测
        self.kf.predict(dt)
        self.kf.update(np.array([point.x, point.y]))

    def predict(self, t):
        dt = t - self.prev_time
        self.kf.predict(dt)
        ans = self.kf.get_state()
        point = Point(ans[0], ans[1])
        # print(f'predict point({id(self)}): {dt}, {point}')
        return point


# class SimpleKalmanFilterWithRelPoint:
#     def __init__(self):
#         self.kf = SimpleKalmanFilter()
#
#     def add_data(self, t, point,rel_point=None, extra=''):
#         if rel_point is not None:
#             point = point.gen_point(-rel_point.x, -rel_point.y)
#         self.kf.add_data(t, point, extra=extra)
#
#     def predict(self, t, rel_point=None):
#         point = self.kf.predict(t)
#         if rel_point is not None:
#             point = point.gen_point(rel_point.x, rel_point.y)
#         return point

# 使用数组少的元素匹配数组多的元素, 匹配成功的逻辑是距离最近, 匹配成功的数据不在匹配, 返回匹配关系 {'A_point': 'B_point'}
def match_points(A: list[Point], B: list[Point]):
    if len(A) > len(B):
        original_dict = match_points(B, A)
        reversed_dict = {value: key for key, value in original_dict.items()}
        return reversed_dict

    matches = {}
    B_used = []  # 用于标记 B 中已经匹配过的点

    for point_a in A:
        min_distance = float('inf')
        closest_point_b = None

        for point_b in B:
            if point_b not in B_used:  # 只考虑未匹配过的 B 中的点
                d = point_a.get_distance(point_b)
                if d < min_distance:
                    min_distance = d
                    closest_point_b = point_b

        if closest_point_b:  # 如果找到了最近的点
            matches[point_a] = closest_point_b
            B_used.append(closest_point_b)  # 标记该点已匹配
    return matches


# list_a = [Point(0,0), Point(1,0), Point(5,0)]
# list_b = [Point(0,0.1), Point(4,0)]
# for k,v in match_points(list_a, list_b).items():
#     print(k,v)
# print(match_points(list_a, list_b))


class ItemsWithKalmanFilter:
    def __init__(self):
        self.skf_list: list[SimpleKalmanFilter] = []

    def process(self, t, rel_item: YoloItem, target_items: list[YoloItem]) -> list[YoloItem]:
        # t = time.time()

        # 计算各个点的相对坐标
        rel_points = []
        for item in target_items:
            rel_points.append(item.middle_point.gen_point(-rel_item.middle_point.x, -rel_item.middle_point.y))

        # 匹配<kf/item.point>
        kf_points = [kf.prev_point for kf in self.skf_list]
        point_mapping = match_points(kf_points, rel_points)
        # 映射关系转为kf->Item
        kf_2_item = {}
        kf_2_rel_point = {}
        for k, v in point_mapping.items():
            kf_point_idx = kf_points.index(k)
            item_idx = rel_points.index(v)
            kf_2_item[self.skf_list[kf_point_idx]] = target_items[item_idx]
            kf_2_rel_point[self.skf_list[kf_point_idx]] = rel_points[item_idx]

        # 匹配上的滤波器更新最新的观测数据
        for kf in self.skf_list:
            if kf in kf_2_item.keys():
                kf.add_data(t, kf_2_rel_point[kf], kf_2_item[kf])

        # 滤波器少, 补充新的滤波器
        if len(target_items) >= len(self.skf_list):
            for idx, item in enumerate(target_items):
                if item not in kf_2_item.values():
                    kf = SimpleKalmanFilter()
                    kf.add_data(t, rel_points[idx], item)
                    self.skf_list.append(kf)

        # 滤波器数量多, 将缺失的点进行预测
        new_target_items = target_items[:]
        if len(target_items) < len(self.skf_list):
            for kf in self.skf_list:
                if kf not in kf_2_item.keys():
                    rel_point = kf.predict(t)
                    # print('滤波器预测相对坐标({}): {}'.format(id(kf),rel_point))
                    point = rel_point.gen_point(rel_item.middle_point.x, rel_item.middle_point.y)
                    logger.debug(f'滤波器补充坐标: {point}')
                    prev_item = kf.prev_extra
                    # todo: 临时做法,将上次的识别框位移
                    prev_middle_point = prev_item.middle_point
                    prev_item.box.move(point.x - prev_middle_point.x, point.y - prev_middle_point.y)
                    new_target_items.append(prev_item)

        return new_target_items
#
#
# items_kf = ItemsWithKalmanFilter()
#
# def new_test_item( x,y,name=''):
#     return AIItemBase(name,0.9,src_box=Box(0,0,100,100), match_box=Box( x,y, x,y))
#
#
# rel_item = new_test_item(0,0,"rel_item")
# print(rel_item.middle_point)
#
# # item1 = AIItemBase('rel',0.9,match_box=Box(0,0,100,100), src_box=Box(0,0,0,0))
#
# t = time.time()
# items_kf.process(t+1,new_test_item(0,0,),[new_test_item(0,0)])
# items_kf.process(t+2,new_test_item(1,1,),[new_test_item(11,11)])
# items_kf.process(t+3,new_test_item(3,3,),[new_test_item(33,33),new_test_item(34,34)])
# items_kf.process(t+4,new_test_item(4,4,),[new_test_item(44,44), new_test_item(45,45)])
# items_kf.process(t+5,new_test_item(5,5,),[new_test_item(55,55), new_test_item(56,56)])
# items_kf.process(t+6,new_test_item(6,6,),[new_test_item(66,66), new_test_item(67,67)])
#
# # items_kf.process(3,rel_item,[new_test_item(3,3)])
# # items_kf.process(4,rel_item,[new_test_item(4,4)])
#
# # print(items_kf.process(t+7,new_test_item(0,0,),[])[0].middle_point)
# items_ans = items_kf.process(t+7,new_test_item(7,7,),[new_test_item(66,66)])
# for item in items_ans:
#     print(item.middle_point)
# # items_kf.process(t+8,new_test_item(0,0,),[])
# # print(items_kf.process(t+7,new_test_item(0,0,),[])[0].middle_point)
# # items_kf.process(t+7,new_test_item(7,7,),[new_test_item(77,77)])
# # items_kf.process(t+8,new_test_item(8,8,),[new_test_item(88,88)])
# # items_kf.process(t+9,new_test_item(9,9,),[new_test_item(99,99)])
# # print(items_kf.process(t+10,new_test_item(0,0,),[])[0].middle_point)
# # 假设时间戳和观测点 (time, Point) 是一系列输入数据
# # 假设每次输入一个时间戳和一个新的位置点
# print('-------------------------------------')
# observations = [
#     (2, np.array([21,21])),
#     (3, np.array([31,31])),
#     # (2, np.array([2.0, 3.0])),
#     (4, np.array([41,41])),
#     (5, np.array([51,51])),
#     # (5, np.array([5.0, 6.0])),
#     (6, np.array([61, 61])),
# ]
#
# kf = SimpleKalmanFilter()
# for timestamp, point in observations:
#     kf.add_data(timestamp, Point(point[0], point[1]))
# print(f"时间: {7}, 预测位置: {kf.predict(7)}")
# print(f"时间: {8}, 预测位置: {kf.predict(8)}")
#
# # 示例使用
# kf = KalmanFilter()
#
# # 假设时间戳和观测点 (time, Point) 是一系列输入数据
# # 假设每次输入一个时间戳和一个新的位置点
# observations = [
#     (1, np.array([1.0, 1.0])),
#     (2, np.array([2.0, 2.0])),
#     (3, np.array([3.0, 3.0])),
#     (4, np.array([4.0, 4.0])),
#     (5, np.array([5.0, 5.0])),
# ]
#
# previous_time = 0  # 初始化时间戳
#
# for timestamp, point in observations:
#     dt = timestamp - previous_time  # 计算时间差（时间戳之间的差值）
#
#     # 1. 预测步骤：根据时间差 dt 来预测下一个时刻的状态
#     kf.predict(dt)
#     print(f"时间: {timestamp}, 预测位置: {kf.get_state()}")
#
#     # 2. 更新步骤：将新的观测数据输入更新步骤
#     kf.update(point)
#
#     # 输出当前时刻的预测结果
#     print(f"时间: {timestamp}, 预测位置: {kf.get_state()}")
#
#     # 更新当前时间戳
#     previous_time = timestamp
#
# kf.predict(1)
# print(f"时间: {timestamp}, 预测位置: {kf.get_state()}")
