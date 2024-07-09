import svmLoad
import pandas as pd
import os
import time

csv_file_path = 'loadmaster0318.csv'
# 开始计时
start_time = time.time()
# 读取数据，数据格式必须和这个csv一致
data = pd.read_csv(os.path.join(csv_file_path))
#重复调用模型100次
for i in range(100):
    output = svmLoad.svmPredict(data)
# 结束计时
end_time = time.time()
# 计算执行时间
execution_time = end_time - start_time
print('预测结果:', output)
print('svmPredict 函数单次执行时间:', execution_time/100, '秒')




