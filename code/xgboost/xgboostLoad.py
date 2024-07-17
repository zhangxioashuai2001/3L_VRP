import joblib
import pandas as pd
import numpy as np
import os
from typing import List

model_filename = 'xgboost_model.joblib'
loaded_model = joblib.load(model_filename)

# x 是DataFrame, 包含了目标变量(if_loaded)和特征，删除一些特征值,xgboost不需要归一化
def xgboostPredict(x: List) -> List[int]:
    x = x.drop(["if_loaded", "oder_id", 'max_asr', 'aspect_ratio_var'], axis=1)
    y_pred_xgboost: List[int] = loaded_model.predict(x)
    return y_pred_xgboost
