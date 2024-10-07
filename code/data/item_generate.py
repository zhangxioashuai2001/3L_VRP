import numpy as np
import random
import pandas as pd

# 设置随机种子
random.seed(41)

#
# 创造整数尺寸物品，
# container_length = 60
# container_width = 25
# container_height = 30
# 以50+ items_number 为例，先生成sku池，按照5*5*5，即期待落在0.2*0.2*0.2上，L in the interval[0.1,0.3],W,H同理。
# 15+ items_number时，按照L in the interval[0.2,0.6]
# 15- items_number时，按照L in the interval[0.4,0.9]
# small sku:5*7*14种
# medium sku:11*13*25种
# big sku:13*16*31种
# # notice: index reusing inside
# def generate_item(vehicle_length: float,vehicle_width: float,vehicle_height: float):
#     capacity = vehicle_length* vehicle_width* vehicle_height
#     col_namen = ['l', 'w', 'h']
#     sku_pool_small = []
#     sku_pool_medium = []
#     sku_pool_big = []
#
#     # first generate the small_sku_pool
#     l_candidates = []
#     w_candidates = []
#     h_candidates = []
#     l_lower_bound = int(0.1* vehicle_length)
#     l_upper_bound = int(0.3* vehicle_length)
#     w_lower_bound = int(0.1 * vehicle_width)
#     w_upper_bound = int(0.3 * vehicle_width)
#     h_lower_bound = int(0.1 * vehicle_height)
#     h_upper_bound = int(0.3 * vehicle_height)
#     for index in range(l_lower_bound,l_upper_bound+1):
#         l_candidates.append(index)
#     for index in range(w_lower_bound, w_upper_bound+1):
#         w_candidates.append(index)
#     for index in range(h_lower_bound, h_upper_bound+1):
#         h_candidates.append(index)
#     for l in l_candidates:
#         for w in w_candidates:
#             for h in h_candidates:
#                 sku_pool_small.append([l,w,h])
#     sku_pool_small_df = pd.DataFrame(sku_pool_small, columns=col_namen)
#     sku_pool_small_df.to_csv('sku_pool_small.csv')
#
#     # second generate the mediium_sku_pool
#     l_candidates = []
#     w_candidates = []
#     h_candidates = []
#     l_lower_bound = int(0.2* vehicle_length)
#     l_upper_bound = int(0.6* vehicle_length)
#     w_lower_bound = int(0.2 * vehicle_width)
#     w_upper_bound = int(0.6 * vehicle_width)
#     h_lower_bound = int(0.2 * vehicle_height)
#     h_upper_bound = int(0.6 * vehicle_height)
#     for index in range(l_lower_bound,l_upper_bound+1):
#         l_candidates.append(index)
#     for index in range(w_lower_bound, w_upper_bound+1):
#         w_candidates.append(index)
#     for index in range(h_lower_bound, h_upper_bound+1):
#         h_candidates.append(index)
#     for l in l_candidates:
#         for w in w_candidates:
#             for h in h_candidates:
#                 sku_pool_medium.append([l,w,h])
#     sku_pool_medium_df = pd.DataFrame(sku_pool_medium, columns=col_namen)
#     sku_pool_medium_df.to_csv('sku_pool_medium.csv')
#
#     # finally generate the mediium_sku_pool
#     l_candidates = []
#     w_candidates = []
#     h_candidates = []
#     l_lower_bound = int(0.4* vehicle_length)
#     l_upper_bound = int(0.9* vehicle_length)
#     w_lower_bound = int(0.4 * vehicle_width)
#     w_upper_bound = int(0.9 * vehicle_width)
#     h_lower_bound = int(0.4 * vehicle_height)
#     h_upper_bound = int(0.9 * vehicle_height)
#     for index in range(l_lower_bound,l_upper_bound+1):
#         l_candidates.append(index)
#     for index in range(w_lower_bound, w_upper_bound+1):
#         w_candidates.append(index)
#     for index in range(h_lower_bound, h_upper_bound+1):
#         h_candidates.append(index)
#     for l in l_candidates:
#         for w in w_candidates:
#             for h in h_candidates:
#                 sku_pool_big.append([l,w,h])
#     sku_pool_big_df = pd.DataFrame(sku_pool_big, columns=col_namen)
#     sku_pool_big_df.to_csv('sku_pool_big.csv')


def generate_sku_pool(vehicle_length, vehicle_width, vehicle_height, l_range, w_range, h_range, pool_name):
    """
    Generate SKU pool based on given length, width, and height ranges.

    :param vehicle_length: Length of the vehicle/container.
    :param vehicle_width: Width of the vehicle/container.
    :param vehicle_height: Height of the vehicle/container.
    :param l_range: Tuple (lower bound, upper bound) for length.
    :param w_range: Tuple (lower bound, upper bound) for width.
    :param h_range: Tuple (lower bound, upper bound) for height.
    :param pool_name: The name of the SKU pool for output file.
    :return: None
    """
    col_names = ['l', 'w', 'h']
    l_lower_bound, l_upper_bound = int(l_range[0] * vehicle_length), int(l_range[1] * vehicle_length)
    w_lower_bound, w_upper_bound = int(w_range[0] * vehicle_width), int(w_range[1] * vehicle_width)
    h_lower_bound, h_upper_bound = int(h_range[0] * vehicle_height), int(h_range[1] * vehicle_height)

    sku_pool = [
        [l, w, h]
        for l in range(l_lower_bound, l_upper_bound + 1)
        for w in range(w_lower_bound, w_upper_bound + 1)
        for h in range(h_lower_bound, h_upper_bound + 1)
    ]

    sku_pool_df = pd.DataFrame(sku_pool, columns=col_names)
    sku_pool_df.to_csv(f'{pool_name}.csv', index=False)


def generate_item(vehicle_length, vehicle_width, vehicle_height):
    # Small SKU pool
    generate_sku_pool(vehicle_length, vehicle_width, vehicle_height,
                      l_range=(0.1, 0.3), w_range=(0.1, 0.3), h_range=(0.1, 0.3),
                      pool_name='sku_pool_small')

    # Medium SKU pool
    generate_sku_pool(vehicle_length, vehicle_width, vehicle_height,
                      l_range=(0.2, 0.6), w_range=(0.2, 0.6), h_range=(0.2, 0.6),
                      pool_name='sku_pool_medium')

    # Big SKU pool
    generate_sku_pool(vehicle_length, vehicle_width, vehicle_height,
                      l_range=(0.4, 0.9), w_range=(0.4, 0.9), h_range=(0.4, 0.9),
                      pool_name='sku_pool_big')



def run():
    generate_item(60, 25, 30)


if __name__ == "__main__":
    run()



