import pandas as pd
from Item import Item

# 处理第二个文件并创建 Item 对象的函数
def create_items_from_second_file(df):
    grouped_items = {}
    sample_counter = 0  # 样本计数器
    items = []

    for index, row in df.iterrows():
        current_index = int(row['发车号'])  # Assuming the index is in the first column and is an integer

        if index > 0 and current_index != sample_counter:
            grouped_items[sample_counter] = items  # Save items for previous sample
            sample_counter = current_index
            items = []

        l = float(row['SKU长度'])
        w = float(row['SKU宽度'])
        h = float(row['SKU高度'])
        item = Item.from_dimensions_and_fragile(length=l, width=w, height=h, fragile=0)
        items.append(item)



    if sample_counter > 0:
        grouped_items[sample_counter] = items  # 保存最后一个样本的物品

    return grouped_items

# # 加载第二个 Excel 文件
# file_path_2 = 'items.xlsx'
#
# # 读取指定的表格（假设是第一个表格）
# df_2 = pd.read_excel(file_path_2, sheet_name=0)
#
# # 根据第二个文件创建每个样本的物品
# grouped_items_2 = create_items_from_second_file(df_2)
#
# # 示例：如何使用 grouped_items_2 并输出特定样本的 Item 序列
# sample_number = 99  # 需要输出的样本编号
#
# print(f"Items from Sample={sample_number}:")
# if sample_number in grouped_items_2:
#     for item in grouped_items_2[sample_number]:
#         print(item)
# else:
#     print(f"未找到样本 {sample_number} 的物品")
