import json

import pandas as pd
from django.apps import apps

from predict.models import create_table
from predict import IQR
import os


# point是测点名称
def load_all_data(point):
    Windquality = create_table(point)
    raw_data = Windquality.objects.values('datetime', 'status', 'value').order_by('datetime')
    df = pd.DataFrame(list(raw_data))
    # data = []
    # for Windquality in raw_data:
    #     data.append({
    #         'datetime': Windquality.datetime,
    #         'status': Windquality.status,
    #         'value': Windquality.value
    #     })
    # df = pd.DataFrame(data)
    return df


def load_latest_data(point):
    Windquality = create_table(point)
    raw_data = Windquality.objects.values('datetime', 'status', 'value').order_by('-datetime').first()
    if raw_data:
        df = pd.DataFrame([raw_data])
    else:
        df = pd.DataFrame()
    return df

def train_model(train_points, test_points):
    # print(os.getcwd())
    with open('predict/point_mapping.json', 'r', encoding='utf-8') as f:
        point_mapping = json.load(f)
    train_data = pd.DataFrame()
    test_data = pd.DataFrame()
    if isinstance(train_points, list):
        for point in train_points:
            # point：标准测点   mapped_point：真实测点
            mapped_point = point_mapping[point].lower()
            point_data = load_all_data(mapped_point)  # 加载每个点的数据
            point_data = point_data[['datetime', 'value']]  # 假设数据有日期和value列
            point_data = point_data.rename(columns={'value': f'{point}'})  # 重命名value列为每个point的唯一值列
            if train_data.empty:
                train_data = point_data
            else:
                train_data = pd.merge(train_data, point_data, on='datetime', how='inner')  # 合并到train_data中，仅保留一个日期列
    models = apps.get_models()

    if isinstance(test_points,list):
        for point in test_points:
            mapped_point = point_mapping[point].lower()
            point_data = load_latest_data(mapped_point)
            point_data = point_data[['datetime', 'value']]
            point_data = point_data.rename(columns={'value': f'{point}'})  # 重命名value列为每个point的唯一值列
            if test_data.empty:
                test_data = point_data
            else:
                test_data = pd.merge(test_data, point_data, on='datetime', how='inner')

    # 训练模型
    limit = IQR.wind_power(5, 11, 1.75, train_data)
    wpr = IQR.wind_power_res(limit, test_data)
    msg = IQR.wind_power_logic(wpr, test_data)

    return msg