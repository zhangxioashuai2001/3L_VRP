from sklearn.svm import SVC
import joblib
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
import os
import logging
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_predict, KFold
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score


# 设置日志配置
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()

# 设置全局日志文件路径并初始化日志记录
log_file_path = 'all_results_log.txt'
file_handler = logging.FileHandler(log_file_path, mode='w')  # 'w' 表示覆盖文件，使用 'a' 表示追加
logger.addHandler(file_handler)

# 数据归一化的小工具
scaler = MinMaxScaler()

# 文件路径
item_size_list = ['big', 'medium', 'small']
type_rate_list = [0.1, 0.3, 0.5, 0.7, 1.0]

for item_size in item_size_list:
    for type_rate in type_rate_list:
        csv_file_path = f'training{item_size}{type_rate}.csv'

        # 读取数据
        loadmaster = pd.read_csv(csv_file_path, encoding='GBK')

        # 计算并打印全局 if_loaded 的平均值
        global_mean = loadmaster['if_loaded'].mean()
        logger.info(f"数据集: {item_size}, 类型比例: {type_rate}")
        logger.info("全局 if_loaded 的平均值:")
        logger.info(f"{global_mean}\n")

        # 计算并打印全局容积率的平均值
        global_mean = (loadmaster['total_skuvolume'].mean()) / (loadmaster['vehicle_capacity'].mean())
        global_max = (loadmaster['total_skuvolume'].max()) / (loadmaster['vehicle_capacity'].mean())
        global_min = (loadmaster['total_skuvolume'].min()) / (loadmaster['vehicle_capacity'].mean())
        logger.info("全局容积率的平均值、最大值、最小值:")
        logger.info(f"{global_mean}, {global_max}, {global_min}\n")

        # 提取特征和目标变量
        X, y = loadmaster.drop(["if_loaded", "orderid", 'max_asr', 'aspect_ratio_var',
                                'vehicle_length', 'vehicle_width', 'vehicle_height',
                                'vehicle_capacity', '发车号'], axis=1), loadmaster['if_loaded']

        # 对特征进行归一化
        X = scaler.fit_transform(X)

        # 按照3:1划分训练集和测试集
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

        # 创建SVM分类器对象，其中参数已经是svmParamTune调整出的最优结果
        svm_classifier = SVC(kernel='linear', C=10, class_weight={1: 1}, random_state=42)

        # 训练SVM模型
        svm_classifier.fit(X_train, y_train)

        # 在测试集上进行预测
        y_pred_svm = svm_classifier.predict(X_test)

        # 计算并打印准确率、精确率和召回率
        accuracy_svm = accuracy_score(y_test, y_pred_svm)
        precision_svm = precision_score(y_test, y_pred_svm)
        recall_svm = recall_score(y_test, y_pred_svm)
        logger.info(f"SVM Test Accuracy: {accuracy_svm}")
        logger.info(f"SVM Test Precision: {precision_svm}")
        logger.info(f"SVM Test Recall: {recall_svm}")

        # 计算并打印混淆矩阵
        conf_matrix_svm = confusion_matrix(y_test, y_pred_svm)
        logger.info("SVM Test Confusion Matrix:")
        logger.info(f"{conf_matrix_svm}\n")

        # 使用10折交叉验证
        kf = KFold(n_splits=10, shuffle=True, random_state=42)
        y_pred = cross_val_predict(svm_classifier, X_train, y_train, cv=kf)

        # 计算并打印准确率、精确率和召回率
        accuracy = accuracy_score(y_train, y_pred)
        precision = precision_score(y_train, y_pred)
        recall = recall_score(y_train, y_pred)
        logger.info(f"Training Accuracy: {accuracy}")
        logger.info(f"Training Precision: {precision}")
        logger.info(f"Training Recall: {recall}")

        # 计算并打印混淆矩阵
        conf_matrix = confusion_matrix(y_train, y_pred)
        logger.info("Training 10-Folds Confusion Matrix:")
        logger.info(f"{conf_matrix}\n")

        # 各个特征的支持向量权重
        svm_coefs = svm_classifier.coef_
        feature_names = loadmaster.drop(["if_loaded", "orderid", 'max_asr',
                                         'aspect_ratio_var', '发车号'], axis=1).columns

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

        # 保存图表
        plt.savefig(f'feature_importance_{item_size}_{type_rate}.png')
        plt.close()

# 关闭文件处理器
logger.removeHandler(file_handler)
file_handler.close()