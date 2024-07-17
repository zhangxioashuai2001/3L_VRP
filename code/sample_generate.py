from  Tabu_Packing import tabu_packing
from multiprocessing import Pool
from  data_read_for_random_sampling import create_items_from_second_file
import pandas as pd
import time
from Item import  Item,sort_items
import re
from DBLFPOINTS import  plot_packing ,dblf_packing_with_points
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
    generate_order(container_length,container_width,container_height)
    file_path_2 = 'items.xlsx'

    # 读取指定的表格（假设是第一个表格）
    df = pd.read_excel(file_path_2, sheet_name=0)
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
    df.to_excel(file_path_2, index=False)
    # 计算并打印按 load_parameter 聚合的 if_loaded 平均数
    group_mean = df.groupby('load_parameter')['if_loaded'].mean()
    print("Grouped mean if_loaded by load_parameter:")
    print(group_mean)

    # 计算并打印全局 if_loaded 的平均值
    global_mean = df['if_loaded'].mean()
    print("Global mean if_loaded:")
    print(global_mean)


    # # 选择要处理的组
    # group_ids = [1,2,3,4, 5,6,7,8,9,10,11,12]
    # # 使用多进程池
    # with Pool(processes=len(group_ids)) as pool:
    #     results = []
    #     for group_id in group_ids:
    #         items = grouped_items[group_id]
    #         result = pool.apply_async(process_group, (group_id, items, container_length, container_width, container_height))
    #         results.append(result)
    #     #
    #     # 获取结果
    #     for result in results:
    #         print(result.get())

if __name__ == "__main__":
    main()


