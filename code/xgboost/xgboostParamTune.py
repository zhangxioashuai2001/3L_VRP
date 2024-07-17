import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_predict, KFold
from sklearn.metrics import accuracy_score, confusion_matrix
import xgboost as xgb
from imblearn.over_sampling import RandomOverSampler
from imblearn.pipeline import Pipeline
import joblib
from sklearn.model_selection import GridSearchCV

# 文件路径
csv_file_path = 'training.csv'

# 读取数据
loadmaster = pd.read_csv(os.path.join(csv_file_path),encoding='gbk')

# 提取特征和目标变量
X, y = loadmaster.drop(["if_loaded","orderid",'max_asr','aspect_ratio_var','发车号'], axis=1), loadmaster['if_loaded']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# 创建xgboost分类器对象
pipeline=Pipeline([('classification', xgb.XGBClassifier())])
# 定义参数网格
parameters = {
    'classification__max_depth': [3, 5, 7],  # 树的最大深度
    'classification__learning_rate': [0.1, 0.01, 0.001],  # 学习率
    'classification__n_estimators': [50, 100, 200],  # 树的数量
    'classification__gamma': [0, 0.1, 0.2],  # gamma参数
    'classification__reg_lambda': [0, 1, 10]  # reg_lambda参数
}

# 使用GridSearchCV进行参数调优
grid_search = GridSearchCV(pipeline, parameters, cv=10)  # 十折交叉验证
grid_search.fit(X_train, y_train)
# 输出最佳参数
print("Best parameters:", grid_search.best_params_)

# 输出交叉验证的平均准确率
print("Cross-validation mean accuracy:", grid_search.best_score_)
