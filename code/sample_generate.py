from Tabu_Packing import tabu_packing
from multiprocessing import Pool
from data_read_for_random_sampling import create_items_from_second_file
import pandas as pd
import time
from Item import Item, sort_items
import re
from DBLFPOINTS import plot_packing, dblf_packing_with_points
from MTA import mta
from data_generate import generate_order


def process_group(group_id, items, container_length, container_width, container_height):
    start_time = time.time()
    sort_items(items)
    result = dblf_packing_with_points(items, container_length, container_width, container_height)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Group {group_id} took {elapsed_time:.2f} seconds")
    # plot_packing(items, container_length / 2, container_width, container_height)
    return group_id, result, elapsed_time


def main():
    container_width = 25
    container_height = 30
    container_length = 60
    # item_size='big'
    # type_rate=0.1
    type_rate_list = [0.1, 0.3, 0.5, 0.7, 1.0]
    item_size_list = ['big','medium','small']
    # generate_order(container_length,container_width,container_height)
    for item_size in item_size_list:
        for type_rate in type_rate_list:

            file_path_2 = f'data/{item_size}_items_type_rate{type_rate}.csv'

            df = pd.read_csv(file_path_2)
            # Create items for each group
            grouped_items = create_items_from_second_file(df)

            for i in range(5000):
                # if  (i == 5 or i == 4):
                #     continue

                items = grouped_items[i]
                sort_items(items)
                print(len(items))
                container_width = 25
                container_height = 30
                container_length = 60
                print(i)
                result = dblf_packing_with_points(items, container_length, container_width, container_height)
                # plot_packing(items, container_length / 2, container_width, container_height)
                df.loc[df['发车号'] == i, '车辆总容积(m3)'] = container_length * container_width * container_height
                # 根据 result[0] 填充 if_loaded 列
                if result[0]:
                    df.loc[df['发车号'] == i, 'if_loaded'] = 1
                else:
                    df.loc[df['发车号'] == i, 'if_loaded'] = 0

                print(result)

                # 保存更新后的 DataFrame 到 Excel 文件

            df.to_csv(file_path_2)
            # 计算并打印按 load_parameter 聚合的 if_loaded 平均数
            group_mean = df.groupby('load_parameter')['if_loaded'].mean()
            print("Grouped mean if_loaded by load_parameter:")
            print(group_mean)

            # 计算并打印全局 if_loaded 的平均值
            global_mean = df['if_loaded'].mean()
            print("Global mean if_loaded:")
            print(global_mean)



if __name__ == "__main__":
    main()
