from sklearn.svm import SVC
import joblib
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_predict, KFold
from sklearn.metrics import accuracy_score, confusion_matrix

# 数据归一化的小工具
scaler = MinMaxScaler()
# 文件路径
csv_file_path = 'loadmaster0318.csv'
# 读取数据
loadmaster = pd.read_csv(os.path.join(csv_file_path))
# 提取特征和目标变量
X, y = loadmaster.drop(["if_loaded","oder_id",'max_asr','aspect_ratio_var'], axis=1), loadmaster['if_loaded']
print(y)
# 对特征进行归一化
X = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# 定义SVM分类器对象
svm_classifier = SVC()

# 定义参数网格
param_grid = {
    'C': [ 0.1,0.5, 1, 5, 10],
    'kernel': ['linear','poly'],
}

# 使用GridSearchCV进行参数调优
grid_search = GridSearchCV(svm_classifier, param_grid, cv=10)

# 在训练数据上拟合GridSearchCV
grid_search.fit(X_train, y_train)

# 输出最佳参数
print("Best parameters:", grid_search.best_params_)

# 输出交叉验证的平均准确率
print("Cross-validation mean accuracy:", grid_search.best_score_)