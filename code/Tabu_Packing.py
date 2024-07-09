import random
import time
from typing import List
from copy import deepcopy
from Item import Item, items_overlap, sort_items
from DBLFPOINTS import dblf_packing_with_points,plot_packing
from MTA import mta
# from MTA import MTA


def compute_score_dblf(i, j, count, items, type_1, type_2, tabu_counts: List[int], container_length, container_width,
                       container_height)->float:
    items_tmp = deepcopy(items)
    tmp = items_tmp[i]
    items_tmp[i] = items_tmp[j + len(type_1)]
    items_tmp[j + len(type_1)] = tmp
    length = dblf_packing_with_points(items_tmp, container_length, container_width, container_height)[3]
    if count ==0:
        return length
    penalty = (tabu_counts[i] + tabu_counts[j + len(type_1)]) / count
    return length + penalty * container_length

def compute_score_mta(i, j, count, items, type_1, type_2, tabu_counts: List[int], container_length, container_width,
                       container_height)->float:
    items_tmp = deepcopy(items)
    tmp = items_tmp[i]
    items_tmp[i] = items_tmp[j + len(type_1)]
    items_tmp[j + len(type_1)] = tmp
    length = mta(items_tmp, container_length, container_width, container_height)[3]
    if count ==0:
        return length
    penalty = (tabu_counts[i] + tabu_counts[j + len(type_1)]) / count
    return length + penalty * container_length

def interchange(i, j, items, type_1, type_2) -> None:
    items[i], items[j + len(type_1)] = items[j + len(type_1)], items[i]


# tabu_search 用了两种启发式算法 DBLF 和 MTA ，输出分为两块  首先是是否装载成功（bool），其次是装载方案(如果不成功那就是空的列表)
def tabu_packing(items, container_length, container_width, container_height):
    start_time = time.time()
    total_volume = 0
    capacity: float = container_length * container_width * container_height
    for item in items:
        l, w, h = item.get_dimensions()
        total_volume += l * w * h
    # 如果 物品总体积比 车辆容积大，则肯定装不下，返回False 和 空列表

    if total_volume > capacity:
        print('total_volume > capacity')
        return False, []

    # 计算最大迭代次数   we estimate the difficulty of the loading instance by the proportion of the total volume
    # of the items to the volume of the loading space. Let r be this value;
    # if rr0:6, then we set K=150; otherwise, K =max(5,75*(1-r))

    r: float = total_volume / capacity
    k: int = 0
    if r <= 0.6:
        k = 150
    else:
        k = int(max(5, 75 * (1 - r)))
    tabu_length: int = min(10, len(items) // 2)  # 禁忌表的长度
    sort_items(items)
    tabu_set1, tabu_set2 = set(), set()  # 用hashset 可以在O(1)时间复杂度下判断某一个物品是否在禁忌表(set)中
    if_loaded: bool = False
    best_plan: List[Item] = []
    tabu_counts: List[int] = [0] * len(items)
    best_score: float = float('inf')
    print('k',k)
    feasible, type_1, type_2, lambda_final = dblf_packing_with_points(items, container_length,
                                                                      container_width, container_height)
    best_score = lambda_final
    for s in range(k):
        print('s',s)
        print('best_score',best_score)
        feasible, type_1, type_2, lambda_final = dblf_packing_with_points(items, container_length,
                                                                          container_width, container_height)
        best_move = None
        if feasible:
            if_loaded = True
            best_plan = type_1
            print(f'dblf feasible after {s} iteration')
            end_time = time.time()
            print(f"Elapsed time: {end_time - start_time} seconds")
            return if_loaded, best_plan
            # break
        if lambda_final == float('inf'):
            if_loaded = False
            best_plan = []
            print("dblf lambda_final == float('inf'),which means lambda_final > 2 container length")
            break
        moves = [(i, j) for i in range(len(type_1)) for j in range(len(type_2))]
        for move in moves:
            # 禁忌表内和表外的不能交叉交换
            if (items[move[0]] in tabu_set1 and items[len(type_1)+move[1]] not in tabu_set2) or (
                    items[move[0]] not in tabu_set1 and items[len(type_1)+move[1]] in tabu_set2):
                continue
            # 不同fragile、visit_order的不能交换
            if (items[move[0]].visit_order != items[len(type_1)+move[1]].visit_order) or (items[move[0]].fragile != items[len(type_1)+move[1]].fragile):
                continue
            tmp_score = compute_score_dblf(move[0], move[1], s, items, type_1, type_2, tabu_counts, container_length,
                                           container_width, container_height)
            if tmp_score < best_score:
                best_score = tmp_score
                best_move = move
        if best_move:
            i, j = best_move
            interchange(best_move[0], best_move[1], items, type_1, type_2)
            tabu_counts[i] += 1
            tabu_counts[j + len(type_1)] +=1
            tabu_set1.add(items[i])
            if len(tabu_set1) > tabu_length:
                tabu_set1.pop()
            tabu_set2.add(items[j + len(type_1)])
            if len(tabu_set1) > tabu_length:
                tabu_set1.pop()
        else:
            print(f'dblf no improvement after all{len(moves)} possible moves after {s} iteration')
            break
    end_time = time.time()
    print(f"Elapsed time: {end_time - start_time} seconds")
    # 用MTA进行搜索
    feasible, type_1, type_2, lambda_final = mta(items, container_length, container_width, container_height)
    best_score = lambda_final
    for s in range(k//3):
        print('s', s)
        print('best_score', best_score)
        feasible, type_1, type_2, lambda_final = mta(items, container_length, container_width, container_height)
        best_move = None
        if feasible:
            if_loaded = True
            best_plan = type_1
            print(f'mta feasible after {s} iteration')
            end_time = time.time()
            print(f"Elapsed time: {end_time - start_time} seconds")
            return if_loaded, best_plan
            break
        if lambda_final == float('inf'):
            if_loaded = False
            best_plan = []
            print("lambda_final == float('inf'),which means lambda_final > 2 container length")
            break
        moves = [(i, j) for i in range(len(type_1)) for j in range(len(type_2))]
        for move in moves:
            # 禁忌表内和表外的不能交叉交换
            if (items[move[0]] in tabu_set1 and items[len(type_1) + move[1]] not in tabu_set2) or (
                    items[move[0]] not in tabu_set1 and items[len(type_1) + move[1]] in tabu_set2):
                continue
            # 不同fragile、visit_order的不能交换
            if (items[move[0]].visit_order != items[len(type_1) + move[1]].visit_order) or (
                    items[move[0]].fragile != items[len(type_1) + move[1]].fragile):
                continue
            tmp_score = compute_score_mta(move[0], move[1], s, items, type_1, type_2, tabu_counts, container_length,
                                           container_width, container_height)
            if tmp_score < best_score:
                best_score = tmp_score
                best_move = move
        if best_move:
            i, j = best_move
            interchange(best_move[0], best_move[1], items, type_1, type_2)
            tabu_counts[i] += 1
            tabu_counts[j + len(type_1)] += 1
            tabu_set1.add(items[i])
            if len(tabu_set1) > tabu_length:
                tabu_set1.pop()
            tabu_set2.add(items[j + len(type_1)])
            if len(tabu_set1) > tabu_length:
                tabu_set1.pop()
        else:
            print(f'mta no improvement after all{len(moves)} possible moves after {s} iteration')
            break
    end_time = time.time()
    print(f"Elapsed time: {end_time - start_time} seconds")
    return if_loaded, best_plan

# # Example usage:
# random.seed(1)  # For reproducibility
# items = [
#     # Item.from_dimensions_and_fragile(random.randint(1, 4), random.randint(1, 3), random.randint(1, 4),
#     #                                  random.randint(0, 1)) for _ in range(16)
#     Item.from_dimensions_and_fragile(random.uniform(1,2), random.uniform(1,2), random.randint(1, 2),
#                                      random.randint(0, 1)) for _ in range(50)
# ]
# container_width = 4
# container_height = 4
# container_length = 15.2
# print(tabu_packing(items, container_length,container_width,container_height))
# plot_packing(items, container_length,container_width,container_height)
