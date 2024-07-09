import pandas as pd
from Item import  Item
import re


# Function to process LWH_NI column and create Item objects for each group
def create_items_from_lwh_ni_grouped(df):
    grouped_items = {}

    # Group by 'Sheet' and 'Sample' columns
    grouped = df.groupby(['Sheet', 'Sample'])

    for group_name, group_df in grouped:
        sheet_value, sample_value = group_name
        items = []
        for lwh in group_df['LWH_NI']:
            # Parse the LWH_NI string assuming format "[L W H]"
            lwh_values = re.findall(r"[\d\.]+", lwh)
            l, w, h = map(float, lwh_values)
            item = Item.from_dimensions_and_fragile(length=l, width=w, height=h,fragile=0)
            items.append(item)
        grouped_items[(sheet_value, sample_value)] = items

    return grouped_items



#
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
# grouped_items = create_items_from_lwh_ni_grouped(df)
#
# print("Items from Sheet=1, Sample=1:")
# if (1, 1) in grouped_items:
#     for item in grouped_items[(1, 1)]:
#         print(item)
# else:
#     print("No items found for Sheet=1, Sample=1")