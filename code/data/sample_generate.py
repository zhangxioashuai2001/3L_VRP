import random

# from  Tabu_Packing import tabu_packing
# from multiprocessing import Pool
# from  data_read_for_random_sampling import create_items_from_second_file
import pandas as pd
import numpy as np
# import time
# import re
# from DBLFPOINTS import  plot_packing ,dblf_packing_with_points
# from MTA import mta
# from data_generate import generate_order
random.seed(41)

# 从sku池中选出item_type_cnt种，随机选
# 然后循环直到新添加的这一小组物品体积超出cap*discount，每小组物体数 小[1,10],中[1,3],大[1,2](大多为1)



def generate_samples(vehicle_length, vehicle_width, vehicle_height, size_type, sample_cnt):
    """
    Generate samples from sku pools

    :param vehicle_length: int: Length of the vehicle/container.
    :param vehicle_width: int: Width of the vehicle/container.
    :param vehicle_height: int: Height of the vehicle/container.
    :param size_type: string: Size-Type of items.
    :param sample_cnt: int: Count of samples to generate.
    :return: None
    """
    type_cnt_rate_list = [1.0, 0.7, 0.5, 0.3, 0.1]
    sku_pool = pd.read_csv(f'sku_pool_{size_type}.csv')
    column_names = ['发车号', 'if_loaded', 'SKU长度', 'SKU宽度', 'SKU高度', 'load_parameter', '车辆总容积(m3)']
    vehicle_capacity = vehicle_length* vehicle_width* vehicle_height
    if size_type == 'small':
        ord_cnt_range = (1,11)
        item_cnt_range = (50,150)
    elif size_type == 'medium':
        ord_cnt_range = (1,4)
        item_cnt_range = (15, 50)
    elif size_type == 'big':
        ord_cnt_range = (1,3)
        item_cnt_range = (1, 15)
    for type_cnt_rate in type_cnt_rate_list:
        data = []
        for i in range(sample_cnt):
            item_cnt = random.randint(item_cnt_range[0],item_cnt_range[1])
            item_type_cnt = int(item_cnt * type_cnt_rate)
            possible_values = np.arange(0.6, 1.01, 0.01)
            load_parameter = random.choice(possible_values)
            switch: bool = True
            volume = 0
            recorded = False  # 标志位
            while switch:
                random_skus = sku_pool.sample(n=max(1,item_type_cnt))
                resampled_skus = random_skus.sample(n=max(1,item_cnt), replace=True)

                # 提取每次抽样的 l, w, h 值
                for index, row in resampled_skus.iterrows():
                    l = row['l']
                    w = row['w']
                    h = row['h']
                    # print(f"Resampled l: {l}, w: {w}, h: {h}")
                    volume += l * w * h
                    if volume <= vehicle_capacity * load_parameter:

                        data.append([i, 0, l, w, h, load_parameter, vehicle_capacity])
                        recorded = True
                    elif volume > vehicle_capacity * load_parameter and index ==0:

                        data.append([i, 0, 0, 0, 0, load_parameter, vehicle_capacity])
                        recorded = True
                    else:
                        switch = False

                        break
    # 确保每个发车号都记录下来
            if not recorded:
                data.append([i, 0, l, w, h, load_parameter, vehicle_capacity])
                print(i,volume,l, w, h, load_parameter, vehicle_capacity)
        df = pd.DataFrame(data, columns=column_names)
        print(f'generating {size_type}_items_type_rate{type_cnt_rate}.csv')
        df.to_csv(f'{size_type}_items_type_rate{type_cnt_rate}.csv')


def run():
    generate_samples(60, 25, 30, 'big', 5000)
    # generate_samples(60, 25, 30, 'medium', 5000)
    # generate_samples(60, 25, 30, 'small', 5000)



if __name__ == "__main__":
    run()


