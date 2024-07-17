# import numpy as np
# import random
# import pandas as pd
# from Item import Item
#
# # 设置随机种子
# random.seed(41)
#
#
# def generate_order(vehicle_length: float, vehicle_width: float, vehicle_height: float):
#     discount = [0.6, 0.65, 0.7, 0.75]
#     sample_ratios = [0.1, 0.5, 0.3, 0.1]
#     capacity = vehicle_length * vehicle_width * vehicle_height
#     column_names = ['发车号', 'if_loaded', 'SKU长度', 'SKU宽度', 'SKU高度','load_parameter','车辆总容积(m3)']
#     df = pd.DataFrame(columns=column_names)
#     for i in range(1000):
#         volume = 0
#         load_parameter = random.choices(discount, weights=sample_ratios, k=1)[0]
#         print(load_parameter)
#         while True:
#             tmp_random = np.random.randint(1, 10, 1)
#             if tmp_random == 1:
#                 l = random.uniform(0.1 * vehicle_length, 0.2 * vehicle_length)
#                 w = random.uniform(0.1 * vehicle_width, 0.2 * vehicle_width)
#                 h = random.uniform(0.4 * vehicle_height, 0.9 * vehicle_height)
#                 volume += l * w * h
#                 if volume <= capacity*load_parameter:
#                     new_row = pd.DataFrame({
#                         '发车号': [i],
#                         'SKU长度': [l],
#                         'SKU宽度': [w],
#                         'SKU高度': [h],
#                         'load_parameter': [load_parameter]
#                     })
#                     df = pd.concat([df, new_row], ignore_index=True)
#                 else:
#                     break
#             elif tmp_random == 2:
#                 l = random.uniform(0.4 * vehicle_length, 0.9 * vehicle_length)
#                 w = random.uniform(0.1 * vehicle_width, 0.2 * vehicle_width)
#                 h = random.uniform(0.4 * vehicle_height, 0.9 * vehicle_height)
#                 volume += l * w * h
#                 if volume <= capacity*load_parameter:
#                     new_row = pd.DataFrame({
#                         '发车号': [i],
#                         'SKU长度': [l],
#                         'SKU宽度': [w],
#                         'SKU高度': [h],
#                         'load_parameter': [load_parameter]
#                     })
#                     df = pd.concat([df, new_row], ignore_index=True)
#                 else:
#                     break
#             elif tmp_random == 3:
#                 l = random.uniform(0.2 * vehicle_length, 0.5 * vehicle_length)
#                 w = random.uniform(0.1 * vehicle_width, 0.2 * vehicle_width)
#                 h = random.uniform(0.4 * vehicle_height, 0.9 * vehicle_height)
#                 volume += l * w * h
#                 if volume <= capacity*load_parameter:
#                     new_row = pd.DataFrame({
#                         '发车号': [i],
#                         'SKU长度': [l],
#                         'SKU宽度': [w],
#                         'SKU高度': [h],
#                         'load_parameter': [load_parameter]
#                     })
#                     df = pd.concat([df, new_row], ignore_index=True)
#                 else:
#                     break
#             elif tmp_random == 4:
#                 l = random.uniform(0.1 * vehicle_length, 0.3 * vehicle_length)
#                 w = random.uniform(0.2 * vehicle_width, 0.5 * vehicle_width)
#                 h = random.uniform(0.2 * vehicle_height, 0.5 * vehicle_height)
#                 volume += l * w * h
#                 if volume <= capacity*load_parameter:
#                     new_row = pd.DataFrame({
#                         '发车号': [i],
#                         'SKU长度': [l],
#                         'SKU宽度': [w],
#                         'SKU高度': [h],
#                         'load_parameter': [load_parameter]
#                     })
#                     df = pd.concat([df, new_row], ignore_index=True)
#                 else:
#                     break
#             elif tmp_random == 5:
#                 l = random.uniform(0.2 * vehicle_length, 0.5 * vehicle_length)
#                 w = random.uniform(0.2 * vehicle_width, 0.5 * vehicle_width)
#                 h = random.uniform(0.2 * vehicle_height, 0.5 * vehicle_height)
#                 volume += l * w * h
#                 if volume <= capacity*load_parameter:
#                     new_row = pd.DataFrame({
#                         '发车号': [i],
#                         'SKU长度': [l],
#                         'SKU宽度': [w],
#                         'SKU高度': [h],
#                         'load_parameter': [load_parameter]
#                     })
#                     df = pd.concat([df, new_row], ignore_index=True)
#                 else:
#                     break
#             elif tmp_random == 6:
#                 l = random.uniform(0.4 * vehicle_length, 0.9 * vehicle_length)
#                 w = random.uniform(0.2 * vehicle_width, 0.5 * vehicle_width)
#                 h = random.uniform(0.2 * vehicle_height, 0.5 * vehicle_height)
#                 volume += l * w * h
#                 if volume <= capacity*load_parameter:
#                     new_row = pd.DataFrame({
#                         '发车号': [i],
#                         'SKU长度': [l],
#                         'SKU宽度': [w],
#                         'SKU高度': [h],
#                         'load_parameter': [load_parameter]
#                     })
#                     df = pd.concat([df, new_row], ignore_index=True)
#                 else:
#                     break
#             elif tmp_random == 7:
#                 l = random.uniform(0.1 * vehicle_length, 0.2 * vehicle_length)
#                 w = random.uniform(0.4 * vehicle_width, 0.9 * vehicle_width)
#                 h = random.uniform(0.1 * vehicle_height, 0.2 * vehicle_height)
#                 volume += l * w * h
#                 if volume <= capacity*load_parameter:
#                     new_row = pd.DataFrame({
#                         '发车号': [i],
#                         'SKU长度': [l],
#                         'SKU宽度': [w],
#                         'SKU高度': [h],
#                         'load_parameter': [load_parameter]
#                     })
#                     df = pd.concat([df, new_row], ignore_index=True)
#                 else:
#                     break
#             elif tmp_random == 8:
#                 l = random.uniform(0.4 * vehicle_length, 0.9 * vehicle_length)
#                 w = random.uniform(0.4 * vehicle_width, 0.9 * vehicle_width)
#                 h = random.uniform(0.1 * vehicle_height, 0.2 * vehicle_height)
#                 volume += l * w * h
#                 if volume <= capacity*load_parameter:
#                     new_row = pd.DataFrame({
#                         '发车号': [i],
#                         'SKU长度': [l],
#                         'SKU宽度': [w],
#                         'SKU高度': [h],
#                         'load_parameter': [load_parameter]
#                     })
#                     df = pd.concat([df, new_row], ignore_index=True)
#                 else:
#                     break
#             elif tmp_random == 9:
#                 l = random.uniform(0.2 * vehicle_length, 0.5 * vehicle_length)
#                 w = random.uniform(0.4 * vehicle_width, 0.9 * vehicle_width)
#                 h = random.uniform(0.1 * vehicle_height, 0.2 * vehicle_height)
#                 volume += l * w * h
#                 if volume <= capacity*load_parameter:
#                     new_row = pd.DataFrame({
#                         '发车号': [i],
#                         'SKU长度': [l],
#                         'SKU宽度': [w],
#                         'SKU高度': [h],
#                         'load_parameter': [load_parameter]
#                     })
#                     df = pd.concat([df, new_row], ignore_index=True)
#                 else:
#                     break
#     excel_file_path = 'items.xlsx'
#     df.to_excel(excel_file_path, index=True)
#
#
# generate_order(4, 2, 2)


import numpy as np
import random
import pandas as pd
from Item import Item

# 设置随机种子
random.seed(41)


def generate_order(vehicle_length: float, vehicle_width: float, vehicle_height: float):
    discount = [0.72, 0.68, 0.7, 0.75, 0.76]       #容积率
    sample_ratios = [0.1, 0.1, 0.1, 0.2, 0.5]   #采样概率
    # discount = [0.92, 0.8, 0.82, 0.85, 0.86]  # 容积率
    capacity = vehicle_length * vehicle_width * vehicle_height
    column_names = ['发车号', 'if_loaded', 'SKU长度', 'SKU宽度', 'SKU高度', 'load_parameter', '车辆总容积(m3)']
    mean = 0.82 # 正态分布的均值
    std_dev = 0.1  # 正态分布的标准差
    data = []

    for i in range(5000):
        volume = 0
        # load_parameter = random.choices(discount, weights=sample_ratios, k=1)[0]
        load_parameter = max(min(np.random.normal(mean, std_dev), 1.0), 0.6)  # 从正态分布采样并限制在合理范围
        # load_parameter = 0.8
        # print(load_parameter)
        switch : bool = True
        while switch:
            rd1 = random.randint(1, 2)
            if rd1 <= 2:

                l = random.randint(0.2 * vehicle_length, 0.6 * vehicle_length)
                w = random.randint(0.2 * vehicle_width, 0.6 * vehicle_width)
                h = random.randint(0.2 * vehicle_height, 0.6 * vehicle_height)
                mi = random.randint(1, 3)
                volume += mi * l * w * h
                if volume <= capacity * load_parameter:
                    for j in range(mi):
                        data.append([i, True, l, w, h, load_parameter, capacity])
                else:
                    break
            # else:
            #     l = random.randint(0.05 * vehicle_length, 0.2 * vehicle_length)
            #     w = random.randint(0.04 * vehicle_width, 0.2 * vehicle_width)
            #     h = random.randint(0.1 * vehicle_height - 1, 0.2 * vehicle_height)
            #     mi = random.randint(1, 20)
            #     volume += mi * l * w * h
            #     if volume <= capacity * load_parameter:
            #         for j in range(mi):
            #             data.append([i, True, l, w, h, load_parameter, capacity])
            #     else:
            #         break



            # for j in range(mi):
            #     volume += l*w*h
            #     if volume <= capacity * load_parameter:
            #         data.append([i, True, l, w, h, load_parameter, capacity])
            #     else:
            #         switch = False
            #         break

            # tmp_random = np.random.randint(1, 5, 1)
            # mi = random.randint(1, 3)
            # if tmp_random == 1:
            #     l = 0.2 * vehicle_length
            #     w = 0.2 * vehicle_width
            #     h = 0.6 * vehicle_height
            # elif tmp_random == 2:
            #     l = 0.3 * vehicle_length
            #     w = 0.4 * vehicle_width
            #     h = 0.4 * vehicle_height
            # elif tmp_random == 3:
            #     l = 0.8 * vehicle_length
            #     w = 0.3 * vehicle_width
            #     h = 0.2 * vehicle_height
            # elif tmp_random == 4:
            #     l = 0.2 * vehicle_length
            #     w = 0.1 * vehicle_width
            #     h = 0.2 * vehicle_height
            # volume += mi * l * w * h
            # if volume <= capacity * load_parameter:
            #     for j in range(mi):
            #         data.append([i, True, l, w, h, load_parameter, capacity])
            # else:
            #     break



            # tmp_random = np.random.randint(1, 10, 1)
            # if tmp_random == 1:
            #     # l = random.uniform(0.1 * vehicle_length, 0.2 * vehicle_length)
            #     # w = random.uniform(0.1 * vehicle_width, 0.2 * vehicle_width)
            #     # h = random.uniform(0.4 * vehicle_height, 0.9 * vehicle_height)
            #     l = random.randint(0.1 * vehicle_length, 0.2 * vehicle_length)
            #     w = random.randint(0.1 * vehicle_width, 0.2 * vehicle_width)
            #     h = random.randint(0.4 * vehicle_height, 0.9 * vehicle_height)
            #     volume += l * w * h
            #     if volume <= capacity * load_parameter:
            #         data.append([i, True, l, w, h, load_parameter, capacity])
            #     else:
            #         break
            # elif tmp_random == 2:
            #     l = random.randint(0.4 * vehicle_length, 0.9 * vehicle_length)
            #     w = random.randint(0.1 * vehicle_width, 0.2 * vehicle_width)
            #     h = random.randint(0.4 * vehicle_height, 0.9 * vehicle_height)
            #     volume += l * w * h
            #     if volume <= capacity * load_parameter:
            #         data.append([i, True, l, w, h, load_parameter, capacity])
            #     else:
            #         break
            # elif tmp_random == 3:
            #     l = random.randint(0.2 * vehicle_length, 0.5 * vehicle_length)
            #     w = random.randint(0.1 * vehicle_width, 0.2 * vehicle_width)
            #     h = random.randint(0.4 * vehicle_height, 0.9 * vehicle_height)
            #     volume += l * w * h
            #     if volume <= capacity * load_parameter:
            #         data.append([i, True, l, w, h, load_parameter, capacity])
            #     else:
            #         break
            # elif tmp_random == 4:
            #     l = random.randint(0.1 * vehicle_length, 0.3 * vehicle_length)
            #     w = random.randint(0.2 * vehicle_width, 0.5 * vehicle_width)
            #     h = random.randint(0.2 * vehicle_height, 0.5 * vehicle_height)
            #     volume += l * w * h
            #     if volume <= capacity * load_parameter:
            #         data.append([i, True, l, w, h, load_parameter, capacity])
            #     else:
            #         break
            # elif tmp_random == 5:
            #     l = random.randint(0.2 * vehicle_length, 0.5 * vehicle_length)
            #     w = random.randint(0.2 * vehicle_width, 0.5 * vehicle_width)
            #     h = random.randint(0.2 * vehicle_height, 0.5 * vehicle_height)
            #     volume += l * w * h
            #     if volume <= capacity * load_parameter:
            #         data.append([i, True, l, w, h, load_parameter, capacity])
            #     else:
            #         break
            # elif tmp_random == 6:
            #     l = random.randint(0.4 * vehicle_length, 0.9 * vehicle_length)
            #     w = random.randint(0.2 * vehicle_width, 0.5 * vehicle_width)
            #     h = random.randint(0.2 * vehicle_height, 0.5 * vehicle_height)
            #     volume += l * w * h
            #     if volume <= capacity * load_parameter:
            #         data.append([i, True, l, w, h, load_parameter, capacity])
            #     else:
            #         break
            # elif tmp_random == 7:
            #     l = random.randint(0.1 * vehicle_length, 0.2 * vehicle_length)
            #     w = random.randint(0.4 * vehicle_width, 0.9 * vehicle_width)
            #     h = random.randint(0.1 * vehicle_height, 0.2 * vehicle_height)
            #     volume += l * w * h
            #     if volume <= capacity * load_parameter:
            #         data.append([i, True, l, w, h, load_parameter, capacity])
            #     else:
            #         break
            # elif tmp_random == 8:
            #     l = random.randint(0.4 * vehicle_length, 0.9 * vehicle_length)
            #     w = random.randint(0.4 * vehicle_width, 0.9 * vehicle_width)
            #     h = random.randint(0.1 * vehicle_height, 0.2 * vehicle_height)
            #     volume += l * w * h
            #     if volume <= capacity * load_parameter:
            #         data.append([i, True, l, w, h, load_parameter, capacity])
            #     else:
            #         break
            # elif tmp_random == 9:
            #     l = random.randint(0.2 * vehicle_length, 0.5 * vehicle_length)
            #     w = random.randint(0.4 * vehicle_width, 0.9 * vehicle_width)
            #     h = random.randint(0.1 * vehicle_height, 0.2 * vehicle_height)
            #     volume += l * w * h
            #     if volume <= capacity * load_parameter:
            #         data.append([i, True, l, w, h, load_parameter, capacity])
            #     else:
            #         break

    df = pd.DataFrame(data, columns=column_names)
    excel_file_path = 'items.xlsx'
    df.to_excel(excel_file_path, index=True)


# generate_order(40, 20, 20)
