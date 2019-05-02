# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np
import pandas as pd
import app.server as server
import app.tables as models

db = server.db
features = ['month', 'day', 'hour', 'minute', 'pre_value']
label = 'value'


# split a multivariate sequence into samples
def split_sequences(sequences: pd.DataFrame, n_steps_in: int, n_steps_out: int):
    sequences = sequences.values
    X, y = list(), list()
    for i in range(len(sequences)):
        end_ix = i + n_steps_in
        out_end_ix = end_ix + n_steps_out - 1
        if out_end_ix > len(sequences):
            break
        seq_x, seq_y = sequences[i:end_ix, :-1], sequences[end_ix - 1:out_end_ix, -1]
        X.append(seq_x)
        y.append(seq_y)
    return np.array(X), np.array(y)


# pre power data 추가
def add_pre_power(frame: pd.DataFrame):
    frame = frame[['month', 'day', 'hour', 'minute', 'value']]
    pre_value = list(frame['value'])
    pre_value = [pre_value[0]] + pre_value[:-1]
    frame['pre_value'] = pre_value
    frame = frame[['month', 'day', 'hour', 'minute', 'pre_value', 'value']]
    return frame


def get_power_with_building_id(building_id: int):
    building = db.session.query(models.Building).get(building_id)
    queryset = db.session.query(models.Power).filter_by(buildingId=building.id)
    frame = pd.read_sql_query(queryset.statement, queryset.session.bind)
    frame = add_pre_power(frame)
    return frame
