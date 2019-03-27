# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function
from sklearn.preprocessing import MinMaxScaler
from sklearn.utils import check_array, validation
from datetime import datetime

import pandas as pd


def scale_to_0and1(data):
    data = MinMaxScaler(feature_range=(0, 1)).fit_transform(data)
    return data


def inverse_transform(data, min_, scale_):
    data = check_array(data, dtype=validation.FLOAT_DTYPES, force_all_finite="allow-nan")
    data -= min_
    data /= scale_
    return data


def converter_csv_to_frame(path: str) -> pd.DataFrame:
    time_format = '%m/%d/%Y %H:%M'
    frame = pd.read_csv(path)
    month = frame['Timestamp'].apply(lambda time: datetime.strptime(time, time_format).month)
    day = frame['Timestamp'].apply(lambda time: datetime.strptime(time, time_format). day)
    hour = frame['Timestamp'].apply(lambda time: datetime.strptime(time, time_format).hour)
    minute = frame['Timestamp'].apply(lambda time: datetime.strptime(time, time_format).minute)
    return pd.DataFrame({
        'month': month,
        'day': day,
        'hour': hour,
        'minute': minute,
        'power': frame['Power (kW)']
    })


if __name__ == '__main__':
    frame = converter_csv_to_frame('building.csv')
    print(frame.values)
    frame, scale = scale_to_0and1(frame)

    print(inverse_transform(frame, scale.min_, scale.scale_))

    # scaler = MinMaxScaler(feature_range=(0, 1))
    # print(scale.inverse_transform(frame))
