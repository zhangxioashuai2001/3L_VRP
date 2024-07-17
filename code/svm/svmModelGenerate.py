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
csv_file_path = 'training.csv'
# 读取数据
loadmaster = pd.read_csv(os.path.join(csv_file_path), encoding='GBK')
# 提取特征和目标变量
X, y = loadmaster.drop(["if_loaded", "orderid",'max_asr','aspect_ratio_var','vehicle_length','vehicle_width','vehicle_height','vehicle_capacity','发车号'], axis=1), loadmaster['if_loaded']
# X, y = loadmaster.drop(["if_loaded", "orderid",'max_asr','aspect_ratio_var'], axis=1), loadmaster['if_loaded']
# 对特征进行归一化
print(X)
X = scaler.fit_transform(X)
# 按照3:1划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
# 创建SVM分类器对象，其中参数已经是svmParamTune调整出的最优结果
svm_classifier = SVC(kernel='linear', C=10,class_weight={1: 1.5}, random_state=42)
# 训练SVM模型
svm_classifier.fit(X_train, y_train)
# 在测试集上进行预测
y_pred_svm = svm_classifier.predict(X_test)
# 计算并打印准确率
accuracy_svm = accuracy_score(y_test, y_pred_svm)
print(f"SVM Test Accuracy: {accuracy_svm}")
# 计算并打印混淆矩阵
conf_matrix_svm = confusion_matrix(y_test, y_pred_svm)
print("SVM Test Confusion Matrix:")
print(conf_matrix_svm)


# Use 10-Fold Cross-Validation
kf = KFold(n_splits=10, shuffle=True, random_state=42)
y_pred = cross_val_predict(svm_classifier, X_train, y_train, cv=kf)

# Calculate accuracy
accuracy = accuracy_score(y_train, y_pred)
# print(y_pred, y_train)
print(f"trainingAccuracy: {accuracy}")
# Calculate and print confusion matrix
conf_matrix = confusion_matrix(y_train, y_pred)
print("training 10folds Confusion Matrix:")
print(conf_matrix)




# 各个feature的支持向量权重
svm_coefs = svm_classifier.coef_
# 获取特征名称
# feature_names = loadmaster.drop(["if_loaded", "orderid",'max_asr','aspect_ratio_var','发车号'], axis=1).columns
feature_names = loadmaster.drop(["if_loaded", "orderid",'max_asr','aspect_ratio_var','发车号'], axis=1).columns

# 获取支持向量的系数和特征名称，并按照系数的绝对值降序排列
svm_coefs_abs = np.abs(svm_coefs[0])

sorted_indices = np.argsort(svm_coefs_abs)
sorted_feature_names = feature_names[sorted_indices]
sorted_coefs = svm_coefs_abs[sorted_indices]

# 绘制特征重要性图
plt.figure(figsize=(10, 6))
plt.barh(range(len(sorted_feature_names)), sorted_coefs, align='center')
plt.yticks(np.arange(len(sorted_feature_names)), sorted_feature_names)
plt.xlabel('Coefficient Magnitude')
plt.title('Feature Importance in SVM Model (Sorted)')
plt.show()

