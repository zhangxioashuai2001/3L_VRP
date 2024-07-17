import matplotlib.pyplot as plt
import sys
import time
import pandas as pd
import random
from Item import Item, items_overlap
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from util import slide_item,is_lifo_satisfied,cal_supportarea,is_fragile_satisfied,find_max_X_slide_distance_using_projections,\
    find_max_Y_slide_distance_using_projections,find_max_Z_slide_distance_using_projections
from data_read import create_items_from_lwh_ni_grouped
# 终止条件是所有item全被放下（有可能超出长度限制），或者没有被全部放下但是loading length 已经> 2*container_length了
# 输出分4块  第一块表示是否能装下，bool;第二块表示type1类物品（loading length < container_length,如果第一块为True,则所有物品都是Type1）;
# 第三块表示type2类物品（loading length > container_length）;第四块表示 最后的loading_length
def dblf_packing_with_points(items, container_length, container_width, container_height):
    dblf_start_time = time.time()
    type1_items = []
    type2_items = items[:]  # 一开始将所有物品都设置为Type2
    original_container_length = container_length
    container_length = container_length*2   #如果loading length 超过了两倍车厢长，则终止，表示装不下
    supporting_area_factor: float = 0.3   #底面支撑面积因数，可调
    sp = [(0, 0, 0)]  # starting point
    lambda_final = 0
    placed_items = [Item(0, 0, 0, container_length, container_width, 0,0),
                    Item(0, 0, 0, container_length, 0, container_height,0),
                    Item(0, 0, 0, 0, container_width, container_height,0)]
    for item in items:
        placed = False
        point_best = None
        orientation_best = None
        lambda_global = sys.float_info.max   # 所有物品中最后面的面到车厢前面的距离
        lambda_tmp= sys.float_info.max


        for point in sp:
            for orientation in range(6):
                item.orientation = orientation
                l, w, h = item.get_dimensions()
                if point[0] + l <= container_length and point[1] + w <= container_width and point[2] + h <= container_height:
                # if point[1] + w <= container_width and point[
                #     2] + h <= container_height:
                    item.x, item.y, item.z = point
                    # 表示是否满足这些约束，如果满足约束，则为false
                    overlap = False
                    lifo_violation = False
                    support_area_violation = False
                    fragile_violation = False
                    sup_area_square: float = 0.0
                    # 判断是否满足overlap约束，lifo约束，supporting_area约束，fragile约束
                    for other in placed_items:
                        if items_overlap(item, other):
                            overlap = True
                            break
                    #     if not is_lifo_satisfied(item,other):
                    #         lifo_violation = True
                    #         break
                    #     if not is_fragile_satisfied(item,other):
                    #         fragile_violation = True
                    #         break
                    #     sup_area_square += cal_supportarea(item,other)
                    # support_area_ratio = sup_area_square / (l * w)
                    # if support_area_ratio < supporting_area_factor:
                    #     support_area_violation = True

                    # 将满足约束则将物品按照orientation放置于该position上，并且更新normal position(sp)列表
                    # if not (overlap or lifo_violation or support_area_violation or fragile_violation):
                    if not overlap:
                        # # 如果没有overlap，则尝试平移，平移之后再判断其他约束
                        slide_x = find_max_X_slide_distance_using_projections(item,placed_items)
                        item.x -= slide_x
                        slide_z = find_max_Z_slide_distance_using_projections(item,placed_items)
                        item.z -= slide_z
                        slide_y = find_max_Y_slide_distance_using_projections(item,placed_items)
                        item.y -= slide_y
                        for other in placed_items:
                            if not is_lifo_satisfied(item, other):
                                lifo_violation = True
                                break
                            if not is_fragile_satisfied(item, other):
                                fragile_violation = True
                                break
                            sup_area_square += cal_supportarea(item, other)
                        support_area_ratio = sup_area_square / (l * w)
                        if support_area_ratio < supporting_area_factor:
                            support_area_violation = True

                    if not (overlap or support_area_violation):
                        placed = True
                        lambda_tmp = max(
                            item.x + l,
                            max(
                                other.x + other.get_dimensions()[1]
                                for other in placed_items
                                # if not (other.x == 0 and other.y == 0 and other.z == 0 and other.get_dimensions()[1] == container_width and other.get_dimensions()[0] == container_length)
                            )
                        )
                        if lambda_tmp < lambda_global:
                            lambda_global = lambda_tmp
                            point_best = (item.x,item.y,item.z)
                            orientation_best = orientation
                            lambda_final = lambda_global
                        # print('lambda_global',lambda_global)
            #             placed_items.append(item)
            #             sp.remove(point)
            #             sp.append((item.x + l, item.y, item.z))
            #             sp.append((item.x, item.y + w, item.z))
            #             sp.append((item.x, item.y, item.z + h))
            #             sp = sorted(sp, key=lambda p: (p[0], p[2], p[1]))
            #             placed = True
            #             break
            # if placed:
            #     break
        if placed:
            item.x, item.y, item.z = point_best
            item.orientation = orientation_best
            l, w, h = item.get_dimensions()
            # sp.remove(point_best)
            # 如果还加入了fragile ，lifo ，support area约束 就不要slide了
            # Slide the item in x, y, z directions
            # slide_item(item, container_length, container_width, container_height, placed_items)
            # slide_x = find_max_X_slide_distance_using_projections(item, placed_items)
            # item.x -= slide_x
            # slide_z = find_max_Z_slide_distance_using_projections(item, placed_items)
            # item.z -= slide_z
            # slide_y = find_max_Y_slide_distance_using_projections(item, placed_items)
            # item.y -= slide_y

            placed_items.append(item)
            sp = [p for p in sp if p != point_best]
            sp.append((item.x + l, item.y, item.z))
            sp.append((item.x, item.y + w, item.z))
            sp.append((item.x, item.y, item.z + h))
            sp = sorted(sp, key=lambda p: (p[0], p[2], p[1]))
            if item.x + l <= original_container_length:
                type1_items.append(item)
                type2_items.remove(item)

        if not placed:   # 此时表示loading_length > 2 container_length
            dblf_end_time = time.time()
            print(f"Elapsed time: {dblf_end_time - dblf_start_time} seconds","已经超出两倍车长或无符合约束的可行点")
            item.x, item.y, item.z = None, None, None
            lambda_final = float('inf')
            return False, [(item.x, item.y, item.z, item.orientation) for item in type1_items], [(item.x, item.y, item.z, item.orientation) for item in type2_items],lambda_final
    dblf_end_time = time.time()
    print(f"Elapsed time: {dblf_end_time - dblf_start_time} seconds")
    if not type2_items:  # 此时表示所有物体都被装下 lambda< container_length
        print('装下了')
        print(lambda_final)
        return True, [(item.x, item.y, item.z, item.orientation,item.get_dimensions()) for item in type1_items], [(item.x, item.y, item.z, item.orientation,item.get_dimensions()) for item in type2_items],lambda_final
    else:               # 此时表示 container_length< lambda< 2 container_length
        print(lambda_final)
        return False, [(item.x, item.y, item.z, item.orientation,item.get_dimensions()) for item in type1_items], [(item.x, item.y, item.z, item.orientation,item.get_dimensions()) for item in type2_items],lambda_final


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

    ax.set_xlim([0, container_length*2])  # length is along x-axis
    ax.set_ylim([0, container_width])  # width is along y-axis
    ax.set_zlim([0, container_height])  # height is along z-axis
    # Set equal scaling
    ax.set_box_aspect([container_length*2, container_width, container_height])  # aspect ratio is 1:1:1

    plt.show()


# Example usage:
# random.seed(1)  # For reproducibility
# # items = [
# #     Item.from_dimensions(random.uniform(1, 4), random.uniform(1, 3), random.uniform(1, 5)) for _ in range(8)
# # ]
# items = [
#     Item.from_dimensions_and_fragile(random.randint(1, 4), random.randint(1, 3), random.randint(1, 4),random.randint(0, 1)) for _ in range(20)
# ]
# container_width = 4
# container_height = 4
# container_length = 12

# # Load the Excel file
# file_path = 'D:/OneDrive - stu.hit.edu.cn/桌面/项目/BPP+VRP/未聚合output_resultArea_Height_Asc.xlsx'
#
# sheet_name = 'Sheet1'  # Replace with the actual sheet name if it's different
#
#
# # Read the specified sheet
# df = pd.read_excel(file_path, sheet_name=sheet_name)
#
# # Create items for each group
# items = create_items_from_lwh_ni_grouped(df)[(1,1)]
#
# print(items)
#
# random.seed(1)  # For reproducibility
# # items = [
# #     Item.from_dimensions_and_fragile(random.randint(1, 4), random.randint(1, 3), random.randint(1, 4),
# #                                      random.randint(0, 1)) for _ in range(15)
# # ]
# print(items)
# container_width = 4
# container_height = 4
# container_length = 13.7
#
# feasible, packing_plan,type_2,lambda_final = dblf_packing_with_points(items, container_length, container_width, container_height)
# if feasible:
#     print("Packing plan:", packing_plan,type_2,lambda_final)
#     plot_packing(items, container_length, container_width, container_height)
# else:
#     print("No feasible packing found.")
#     print("type1 Packing plan:", packing_plan,"type2 Packing plan:",type_2,lambda_final)
#     plot_packing(items, container_length, container_width, container_height)
