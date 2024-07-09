from  Tabu_Packing import tabu_packing
from multiprocessing import Pool
from  data_read_new import create_items_from_second_file
import pandas as pd
import time
from Item import  Item,sort_items
import re
from DBLFPOINTS import  plot_packing ,dblf_packing_with_points
from MTA import mta

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
# # Load the Excel file
# file_path = 'D:/OneDrive - stu.hit.edu.cn/桌面/项目/BPP+VRP/未聚合output_resultArea_Height_Asc.xlsx'
#
# sheet_name = 'Sheet1'  # Replace with the actual sheet name if it's different
#
# # Read the specified sheet
    # df = pd.read_excel(file_path, sheet_name=sheet_name)
    file_path_2 = '31组新样例.xlsx'

    # 读取指定的表格（假设是第一个表格）
    df = pd.read_excel(file_path_2, sheet_name=2)
    # Create items for each group
    grouped_items = create_items_from_second_file(df)
    container_width = 2.2
    container_height = 2
    container_length = 4.2


    for i in range(1,24):
        # if  (i == 5 or i == 4):
        #     continue

        items = grouped_items[i]
        sort_items(items)
        # print(items)
        print(len(items))
        container_width = 2.2
        container_height = 2
        container_length = 4.2
        print(dblf_packing_with_points(items, container_length,container_width,container_height))
        print(max(item.length*item.width*items.height) for item in items)
        # plot_packing(items, container_length/2,container_width,container_height)

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


