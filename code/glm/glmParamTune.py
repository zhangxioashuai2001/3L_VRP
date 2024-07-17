from sklearn.linear_model import LogisticRegression
import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split, cross_val_predict, KFold
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import MinMaxScaler

# 数据归一化工具
scaler = MinMaxScaler()

# 文件路径
csv_file_path = 'training.csv'

# 读取数据
loadmaster = pd.read_csv(os.path.join(csv_file_path),encoding='gbk')
X, y = loadmaster.drop(["if_loaded","orderid",'max_asr','aspect_ratio_var'], axis=1), loadmaster['if_loaded']

X = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
# 创建逻辑回归分类器对象
logistic_classifier = LogisticRegression(penalty='l1', solver='liblinear', max_iter=1000)
# 定义要调优的参数范围
param_grid = {
    'C': [0.001, 0.01, 0.1, 1, 10, 100]  # 正则化参数的倒数，较小的值表示更强的正则化
}
# 使用 GridSearchCV 进行十折交叉验证参数调优
grid_search = GridSearchCV(logistic_classifier, param_grid, cv=10, scoring='accuracy')
# 在训练数据上进行网格搜索
grid_search.fit(X_train, y_train)
# 输出最佳参数
print("Best parameters:", grid_search.best_params_)
# 输出交叉验证的平均准确率
print("Cross-validation mean accuracy:", grid_search.best_score_)

# 使用最佳参数的模型在测试集上进行预测
best_logistic_classifier = grid_search.best_estimator_
y_pred_test = best_logistic_classifier.predict(X_test)

# 计算并打印准确率
accuracy_test = accuracy_score(y_test, y_pred_test)
print("Test accuracy with best parameters:", accuracy_test)