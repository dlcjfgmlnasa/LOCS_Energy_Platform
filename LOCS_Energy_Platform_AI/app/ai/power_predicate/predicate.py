# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import copy
import argparse
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from tensorflow.python import keras
from app.ai.power_predicate.model import conv1d


def get_args():
    parser = argparse.ArgumentParser(description='Train power prediction model')
    parser.add_argument('--filters', default=64,
                        help='cnn filter size (default:64)')
    parser.add_argument('--kernel_size', default=20,
                        help='cnn kernel size (default:20)')
    return parser.parse_args()


def get_model(file_path: str, file_name: str):
    n_steps, n_features = 96, 5
    inputs = keras.Input(shape=(n_steps, n_features), name='input_layer')
    model = conv1d(
        inputs=inputs,
        filters=64,
        kernel_size=20
    )
    file_path = os.path.join(file_path, file_name)
    model.load_weights(file_path)
    return model


def predication(model: keras.Model, frame: pd.DataFrame):
    pd_frame = copy.deepcopy(frame)
    pd_frame['value'] = None
    frame_value = frame.values[0]
    year, month, day = int(frame_value[0]), int(frame_value[1]), int(frame_value[2])
    target_day = datetime(year=year, month=month, day=day) + timedelta(days=1)
    pd_frame['year'] = target_day.year
    pd_frame['month'] = target_day.month
    pd_frame['day'] = target_day.day
    frame = frame.append(pd_frame)[['month', 'day', 'hour', 'minute']]
    predicate_values = []
    for start, end in zip(range(96), range(96, len(frame))):
        sample = np.expand_dims(frame[start:end].values, axis=0)
        predicate_value = model.predict(sample)[0][0]

        predicate_values.append(predicate_value)
        break
    return predicate_values



