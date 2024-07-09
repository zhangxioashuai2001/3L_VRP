import matplotlib.pyplot as plt
import random
import time
from util import cal_bottomtop_touching_area, cal_frontback_touching_area, cal_leftright_touching_area, slide_item, \
    is_lifo_satisfied, cal_supportarea, is_fragile_satisfied
from Item import Item, items_overlap
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


# 终止条件是所有item全被放下（有可能超出长度限制），或者没有被全部放下但是loading length 已经> 2*container_length了
# 输出分4块  第一块表示是否能装下，bool;第二块表示type1类物品（loading length < container_length,如果第一块为True,则所有物品都是Type1）;
# 第三块表示type2类物品（loading length > container_length）;第四块表示 最后的loading_length
def mta(items, container_length, container_width, container_height):
    mta_start_time = time.time()
    supporting_area_factor: float = 0.8  # 底面支撑面积因数，可调
    sp = [(0, 0, 0)]
    original_container_length = container_length
    container_length = container_length * 2  # 如果loading length 超过了两倍车厢长，则终止，表示装不下
    type1_items = []
    type2_items = items[:]  # 一开始将所有物品都设置为Type2
    lambda_final = 0
    placed_items = [Item(0, 0, 0, container_length, container_width, 0, 0),
                    Item(0, 0, 0, original_container_length, 0, container_height, 0),
                    Item(0, 0, 0, 0, container_width, container_height, 0)]
    for item in items:
        sr = 0
        s_temp = 0  # 在一个位置一个摆放方向时的一个物品所被接触的面积
        point_best = None
        orientation_best = None
        placed = False
        for point in sp:
            for orientation in range(6):
                s_temp = 0
                item.orientation = orientation
                l, w, h = item.get_dimensions()
                # print(l,w,h,point[1] + w,point)
                if point[0] + l <= container_length and point[1] + w <= container_width and point[
                    2] + h <= container_height:
                    # print(l, w, h, point[1] + w, point, f'placed{placed}', item.x, item.y, item.z)
                    # print(point_best)
                    item.x, item.y, item.z = point
                    overlap = False
                    lifo_violation = False
                    support_area_violation = False
                    fragile_violation = False
                    sup_area_square: float = 0.0
                    # 判断是否满足overlap约束，lifo约束，supporting_area约束，fragile约束
                    for other in placed_items:
                        l2, w2, h2 = other.get_dimensions()
                        if items_overlap(item, other):
                            overlap = True
                            # s_temp = 0
                            break
                        if not is_lifo_satisfied(item, other):
                            lifo_violation = True
                            break
                        if not is_fragile_satisfied(item, other):
                            fragile_violation = True
                            break
                        sup_area_square += cal_supportarea(item, other)
                        if (other == placed_items[0] or other == placed_items[1] or other == placed_items[2]) and item.x > original_container_length:
                            continue
                        if item.z == other.z + h2 or item.z + h == other.z:
                            s_temp += cal_bottomtop_touching_area(item, other)
                        elif item.x == other.x + l2 or item.x + l == other.x:
                            s_temp += cal_frontback_touching_area(item, other)
                        elif item.y == other.y + w2 or item.y + w == other.y:
                            s_temp += cal_leftright_touching_area(item, other)
                    support_area_ratio = sup_area_square / (l * w)
                    if support_area_ratio < supporting_area_factor:
                        support_area_violation = True
                    # if not (overlap or lifo_violation or fragile_violation or support_area_violation):
                    if not (overlap):

                        if s_temp > sr:
                            point_best = point
                            orientation_best = orientation
                            sr = s_temp
                        placed = True

        if placed:
            item.x, item.y, item.z = point_best
            item.orientation = orientation_best
            l, w, h = item.get_dimensions()
            # sp.remove(point_best)
            # 如果还加入了fragile ，lifo ，support area约束 就不要slide了
            slide_item(item, container_length, container_width, container_height, placed_items)
            placed_items.append(item)
            sp = [p for p in sp if p != point_best]
            sp.append((item.x + l, item.y, item.z))
            sp.append((item.x, item.y + w, item.z))
            sp.append((item.x, item.y, item.z + h))
            sp = sorted(sp, key=lambda p: (p[0], p[2], p[1]))
            if item.x + l <= original_container_length:
                type1_items.append(item)
                type2_items.remove(item)
        if not placed:  # 此时表示loading_length > 2 container_length
            mta_end_time = time.time()
            print(f"Elapsed time: {mta_end_time - mta_start_time} seconds")
            item.x, item.y, item.z = None, None, None
            lambda_final = float('inf')
            return False, [(item.x, item.y, item.z, item.orientation) for item in type1_items], \
                   [(item.x, item.y, item.z, item.orientation) for item in type2_items],lambda_final
    for item in placed_items:
        if not (item.x == 0 and item.y == 0 and item.z == 0 and item.get_dimensions()[1] == container_width and
                item.get_dimensions()[0] == container_length):
            lambda_final = max(item.x + item.get_dimensions()[0],lambda_final)
    mta_end_time = time.time()
    print(f"Elapsed time: {mta_end_time - mta_start_time} seconds",lambda_final)

    if not type2_items:  # 此时表示所有物体都被装下 lambda< container_length
        return True, [(item.x, item.y, item.z, item.orientation) for item in type1_items], [
            (item.x, item.y, item.z, item.orientation) for item in type2_items],lambda_final
    else:  # 此时表示 container_length< lambda< 2 container_length
        return False, [(item.x, item.y, item.z, item.orientation) for item in type1_items], [
            (item.x, item.y, item.z, item.orientation) for item in type2_items],lambda_final


def plot_packing(items, container_length, container_width, container_height):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for item in items:
        x = item.x
        y = item.y
        z = item.z
        l, w, h = item.get_dimensions()
        if x is None or y is None or z is None:
            continue

        ax.bar3d(x, y, z, l, w, h, alpha=0.5, color='blue', edgecolor='black')

    ax.set_xlabel('X (Back-Front)')
    ax.set_ylabel('Y (Left-Right)')
    ax.set_zlabel('Z (Bottom-Top)')

    ax.set_xlim([0, 2 * container_length])  # length is along x-axis
    ax.set_ylim([0, container_width])  # width is along y-axis
    ax.set_zlim([0, container_height])  # height is along z-axis
    # Set equal scaling
    ax.set_box_aspect([2 * container_length, container_width, container_height])  # aspect ratio is 1:1:1

    plt.show()


# Example usage:
random.seed(42)  # For reproducibility
# items = [
#     Item.from_dimensions_and_fragile(random.randint(1, 4), random.randint(1, 3), random.randint(1, 5), 0) for _ in
#     range(18)
# ]
#
# container_width = 4
# container_height = 4
# container_length = 10
#
# random.seed(1)  # For reproducibility
# items = [
#     # Item.from_dimensions_and_fragile(random.randint(1, 4), random.randint(1, 3), random.randint(1, 4),
#     #                                  random.randint(0, 1)) for _ in range(16)
#     Item.from_dimensions_and_fragile(random.uniform(1,2), random.uniform(1,2), random.randint(1, 2),
#                                      random.randint(0, 1)) for _ in range(50)
# ]
# container_width = 4
# container_height = 4
# container_length = 14
#
# feasible, packing_plan, type_2 ,lambda_final= mta(items, container_length, container_width, container_height)
# if feasible:
#     print("Packing plan:", packing_plan, type_2,lambda_final)
#     plot_packing(items, container_length, container_width, container_height)
# else:
#     print("No feasible packing found.")
#     print("type1 Packing plan:", packing_plan, "type2 Packing plan:", type_2,lambda_final)
#     plot_packing(items, container_length, container_width, container_height)
