# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import datetime
import numpy as np
import pandas as pd
import app.server as server
import app.tables as models

db = server.db
features = ['month', 'day', 'hour', 'minute', 'pre_value']
label = ['value']
n_features = len(features)


# Split Test / Train dataset
def split_test_train_sequences(data: tuple, split_rate: float):
    x, y = data
    split_index = int(len(x) * (1 - split_rate))
    train_x, train_y = x[:split_index], y[:split_index]
    test_x, test_y = x[split_index:], y[split_index:]
    return train_x, train_y, test_x, test_y


# Split weekday / weekend
def split_weekday_weekend(sequences: pd.DataFrame):
    week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday',  'Friday', 'Saturday']

    def get_weekday(x):
        year = int(x['year'])
        month = int(x['month'])
        day = int(x['day'])
        today = datetime.datetime(year, month, day)
        return week[today.weekday()]
        
    sequences['weekend'] = sequences.apply(lambda x: get_weekday(x), axis=1)
    weekend_flag = (sequences['weekend'] == 'Sunday') | (sequences['weekend'] == 'Saturday')
    weekend_sequences = sequences[weekend_flag][features + label]
    weekday_sequences = sequences[~weekend_flag][features + label]
    return weekday_sequences, weekend_sequences


# split a multivariate sequence into samples
def split_sequences(sequences: pd.DataFrame, n_steps: int):
    # Split weekday / weekend
    weekday_sequences, weekend_sequences = split_weekday_weekend(sequences)
    weekday_sequences = weekday_sequences
    weekend_sequences = weekend_sequences

    def make_dataset(sample):
        # make dataset for training
        sample = sample.values
        X, y = list(), list()
        for i in range(len(sample)):
            in_ix = i + n_steps
            end_ix = in_ix + 1
            if end_ix > len(sample):
                break
            seq_x, seq_y = sample[i:in_ix, :-1], sample[in_ix:end_ix, -1]
            X.append(seq_x)
            y.append(seq_y)
        return np.array(X), np.array(y)

    return make_dataset(weekday_sequences), make_dataset(weekend_sequences)
    # return make_dataset(sequences)


# pre power data 추가
def add_pre_power(frame: pd.DataFrame):
    frame = frame[['year', 'month', 'day', 'hour', 'minute', 'value']]
    pre_value = list(frame['value'])
    pre_value = [pre_value[0]] + pre_value[:-1]
    frame['pre_value'] = pre_value
    frame = frame[['year', 'month', 'day', 'hour', 'minute', 'pre_value', 'value']]
    # frame = frame[['month', 'day', 'hour', 'minute', 'pre_value', 'value']]
    return frame


def get_power_with_building_id(building_id: int):
    building = db.session.query(models.Building).get(building_id)
    queryset = db.session.query(models.Power).filter_by(buildingId=building.id)
    frame = pd.read_sql_query(queryset.statement, queryset.session.bind)
    frame = add_pre_power(frame)
    return frame


# inject db
def inject_db(base_path):
    for building in db.session.query(models.Building).all():
        bld = building.bld
        frame = pd.read_csv(
            os.path.join(base_path, bld + '.csv')
        )
        frame.columns = ['date', 'value']
        time_format = '%Y-%m-%d %H:%M:%S'

        frame['year'] = frame['date'].apply(lambda x: datetime.datetime.strptime(str(x), time_format).year)
        frame['month'] = frame['date'].apply(lambda x: datetime.datetime.strptime(str(x), time_format).month)
        frame['day'] = frame['date'].apply(lambda x: datetime.datetime.strptime(str(x), time_format).day)
        frame['hour'] = frame['date'].apply(lambda x: datetime.datetime.strptime(str(x), time_format).hour)
        frame['minute'] = frame['date'].apply(lambda x: datetime.datetime.strptime(str(x), time_format).minute)
        powers = []
        print(frame)
        for year, month, day, hour, minute, power in frame[['year', 'month', 'day', 'hour', 'minute', 'value']].values:
            powers.append(models.Power(
                year=year,
                month=month,
                day=day,
                hour=hour,
                minute=minute,
                value=power))
        building.powers = powers
        db.session.add(building)
        db.session.commit()


def dummy_power_predicate_value():
    for building in db.session.query(models.Building).all():
        power_queryset = db.session.query(models.Power).\
            filter(models.Power.buildingId == building.id)
        power_frame = pd.read_sql_query(power_queryset.statement, db.session.bind)
        power_value = power_frame['value'].values
        max_ = max(power_value) / 30
        print(np.random.randn(len(power_value)))


if __name__ == '__main__':
    dummy_power_predicate_value()
    # inject_db(
    #     'C://workspace//LOCS_Energy_Platform//locs_energy_platform_ai//app//ai//power_predicate//power_dataset'
    # )
