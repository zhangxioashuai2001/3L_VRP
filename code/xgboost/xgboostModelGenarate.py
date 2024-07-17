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
from sklearn.preprocessing import MinMaxScaler

# 文件路径
csv_file_path = 'training.csv'

# 读取数据
loadmaster = pd.read_csv(os.path.join(csv_file_path),encoding='gbk')

# 提取特征和目标变量
X, y = loadmaster.drop(["if_loaded","orderid",'max_asr','aspect_ratio_var','发车号'], axis=1), loadmaster['if_loaded']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
print(y_test)

#Create the pipeline with XGBoost classifier
pipeline = Pipeline([
    ('classification', xgb.XGBClassifier(
        objective='binary:logistic',
        tree_method='hist',
        eval_metric=['auc', 'logloss'],
        gamma=0.1,
        learning_rate=0.1,
        max_depth=7,
        n_estimators=50,
        reg_lambda=20,
        seed=42
    ))
])
# Use 10-Fold Cross-Validation
kf = KFold(n_splits=10, shuffle=True, random_state=42)
y_pred = cross_val_predict(pipeline.named_steps['classification'], X_train, y_train, cv=kf)

# Calculate accuracy
accuracy = accuracy_score(y_train, y_pred)
# print(y_pred, y_train)
print(f"trainingAccuracy: {accuracy}")
# Calculate and print confusion matrix
conf_matrix = confusion_matrix(y_train, y_pred)
print("training 10folds Confusion Matrix:")
print(conf_matrix)

# 输出importance和测试精度
pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"testAccuracy: {accuracy}")
conf_matrix = confusion_matrix(y_test, y_pred)
print("test Confusion Matrix:")
print(conf_matrix)
fig, ax = plt.subplots(figsize=(20, 20))
xgb.plot_importance(pipeline.named_steps['classification'], ax=ax)
plt.show()
