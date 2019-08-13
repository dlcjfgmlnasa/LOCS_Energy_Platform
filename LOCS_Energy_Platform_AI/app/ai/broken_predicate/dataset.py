# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import matplotlib
import numpy as np
import pandas as pd
import app.server as server
import app.tables as models


matplotlib.use('TkAgg')

db = server.db


def get_power_with_building_id(building_id: int):
    building = db.session.query(models.Building).get(building_id)
    queryset = db.session.query(models.Broken).filter_by(buildingId=building.id)
    frame = pd.read_sql_query(queryset.statement, queryset.session.bind)
    return frame


def data_generator(wave_size: int, size: int, noise_value: float):
    x = np.linspace(-np.pi, np.pi, wave_size)
    y = []
    for _ in range(size):
        sin_y = np.sin(x) + np.random.uniform(-noise_value, noise_value, size=wave_size)
        cos_y = np.cos(x) + np.random.uniform(-noise_value, noise_value, size=wave_size)
        y.extend(sin_y + cos_y)
    return np.array(y)


def split_sequences(sequences: np.array, n_steps: int):
    x, y = [], []
    for i in range(len(sequences) - n_steps + 1):
        first = i
        last = i + n_steps
        x_sample = np.reshape(sequences[first:last], (-1, 1))
        x.append(x_sample)
        y_sample = sequences[first:last]
        y.append(y_sample)
    return np.array(x), np.array(y)
