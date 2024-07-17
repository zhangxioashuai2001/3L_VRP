import joblib
import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from typing import List

# 加载模型, 模型 = LogisticRegression(penalty='l1', solver='liblinear', C=1, random_state=42, max_iter=1000)
model_filename = 'logistic_regression_model.pkl'
loaded_model = joblib.load(model_filename)

# x 是DataFrame, 包含了目标变量(if_loaded)和特征，对特征进行归一化处理并删除一些特征值
def glmPredict(x: List) -> List[int]:
    scaler = MinMaxScaler()
    x = x.drop(["if_loaded", "oder_id", 'max_asr', 'aspect_ratio_var'], axis=1)
    x = scaler.fit_transform(x)
    y_pred_glm: List[int] = loaded_model.predict(x)
    return y_pred_glm
