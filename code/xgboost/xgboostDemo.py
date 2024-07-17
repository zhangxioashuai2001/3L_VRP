import xgboostLoad
import pandas as pd
import os

csv_file_path = 'loadmaster0318.csv'

# 读取数据，数据格式必须和这个csv一致
data = pd.read_csv(os.path.join(csv_file_path))

# 调用模型
output = xgboostLoad.xgboostPredict(data)

print('预测结果:', output)
