from sklearn.linear_model import LogisticRegression
import pandas as pd
import numpy as np
import os
import joblib
import matplotlib.pyplot as plt
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
logistic_classifier = LogisticRegression(penalty='l1', solver='liblinear', C=10, random_state=42, max_iter=1000)

# 训练逻辑回归模型
logistic_classifier.fit(X_train, y_train)

# 在测试集上进行预测
y_pred_logistic = logistic_classifier.predict(X_test)

# 计算并打印准确率
accuracy_logistic = accuracy_score(y_test, y_pred_logistic)
print(f"Logistic Regression Test Accuracy: {accuracy_logistic}")

# 计算并打印混淆矩阵
conf_matrix_logistic = confusion_matrix(y_test, y_pred_logistic)
print("Logistic Regression Test Confusion Matrix:")
print(conf_matrix_logistic)

# 获取特征名称
feature_names = loadmaster.drop(["if_loaded","orderid",'max_asr','aspect_ratio_var'], axis=1).columns

# 获取系数的绝对值并按降序排列
coefs_abs = np.abs(logistic_classifier.coef_[0])
sorted_indices = np.argsort(coefs_abs)
sorted_feature_names = feature_names[sorted_indices]
sorted_coefs = coefs_abs[sorted_indices]

# 绘制特征重要性图
plt.figure(figsize=(10, 6))
plt.barh(range(len(sorted_feature_names)), sorted_coefs, align='center')
plt.yticks(np.arange(len(sorted_feature_names)), sorted_feature_names)
plt.xlabel('Coefficient Magnitude')
plt.title('Feature Importance in Logistic Regression Model (Descending Order)')
plt.show()


# 指定模型保存的文件名
model_filename = 'logistic_regression_model.pkl'

# 保存模型
joblib.dump(logistic_classifier, model_filename)
print(f"Model saved to {model_filename}")