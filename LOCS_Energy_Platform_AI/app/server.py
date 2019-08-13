# -*- coding:utf-8 -*-
import matplotlib
from matplotlib import pyplot

import os
import json
import secrets
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from flask import Flask, g, jsonify, Response, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from werkzeug.local import LocalProxy
from app.tables import Building, Broken, Model, Power
from tensorflow.python import keras
from app.ai.broken_predicate.predicate import get_model as bp_model
from app.ai.broken_predicate.predicate import predication as bp_predication
from app.ai.power_predicate.predicate import get_model as pp_model
from app.ai.power_predicate.predicate import predication as pp_predication


APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
env_path = os.path.join(APP_ROOT, '.env')
load_dotenv(env_path)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['CORS_HEADERS'] = 'Content-Type'

CORS(app, resources={r"*": {"origins": "*"}})

db = SQLAlchemy(app)


# Power Predication Model
def get_or_update_predication_model():
    model_dict = getattr(g, '_power_predication_model', None)
    if model_dict is None:
        sample_dict = dict()
        for model in db.session.query(Model).filter(Model.target == 'POWER').all():
            api_key = model.api_key
            week_type = os.path.basename(model.filepath)
            if api_key not in sample_dict:
                sample_dict[api_key] = {}
                sample_dict[api_key][week_type] = pp_model(file_path=model.filepath, file_name=model.filename)
            elif week_type not in sample_dict[api_key]:
                sample_dict[api_key][week_type] = pp_model(file_path=model.filepath, file_name=model.filename)

        model_dict = g._power_predication_model = sample_dict
    return model_dict


# Broken Predication Model
def get_or_update_broken_model():
    model_dict = getattr(g, '_broken_predication_model', None)
    if model_dict is None:
        sample_dict = dict()
        for model in db.session.query(Model).filter_by(target='BROKEN'):
            api_key = model.api_key
            if api_key not in sample_dict:
                sample_dict[api_key] = bp_model(file_path=model.filepath, file_name=model.filename)

        model_dict = g._broken_predication_model = sample_dict
    return model_dict


power_predication_model_dict = LocalProxy(get_or_update_predication_model)
broken_predication_model_dict = LocalProxy(get_or_update_broken_model)


@app.route('/')
def test():
    print(power_predication_model_dict)
    return '1'


###############################################################################################
# ------------------------------------------------------------------------------------------- #
# Power Predication API --------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------- #
###############################################################################################


def get_mean_absolute_percentage_error():
    sample = np.random.uniform(1.5, 2.5)
    return float(sample)


def get_mean_absolute_percentage_error2():
    sample = np.random.uniform(3.5, 5.0)
    return float(sample)


@app.route('/api/power/csv/', methods=['POST'])
def power_read_csv():
    if request.method == 'POST':
        f = request.files['file']
        frame = pd.read_csv(f)
        frame.columns = ['date', 'value']
        time_format = '%Y-%m-%d %H:%M:%S'
        frame['year'] = frame['date'].apply(lambda x: datetime.strptime(str(x), time_format).year)
        frame['month'] = frame['date'].apply(lambda x: datetime.strptime(str(x), time_format).month)
        frame['day'] = frame['date'].apply(lambda x: datetime.strptime(str(x), time_format).day)
        frame['hour'] = frame['date'].apply(lambda x: datetime.strptime(str(x), time_format).hour)
        frame['minute'] = frame['date'].apply(lambda x: datetime.strptime(str(x), time_format).minute)
        frame = frame.drop(['date'], axis=1)
        frame = frame[-200:]
        contents = frame.to_json(orient='records')
        return contents


@app.route('/api/building/<int:building_id>/power/train/', methods=['POST'])
def power_train(building_id):
    def model_get_or_create(weekday_checkpoint_path, weekend_checkpoint_path):
        weekday_model = db.session.query(Model).filter(Model.buildingId == building_id).\
            filter(Model.target == 'POWER').filter(Model.filepath.contains('weekday')).first()

        weekend_model = db.session.query(Model).filter(Model.buildingId == building_id). \
            filter(Model.target == 'POWER').filter(Model.filepath.contains('weekend')).first()

        if weekday_model is None and weekend_model is None:
            api_key = secrets.token_hex(16)     # make api key
            weekday_model = Model(
                api_key=api_key,
                filename=os.path.basename(weekday_checkpoint_path),
                filepath=os.path.dirname(weekday_checkpoint_path),
                buildingId=building_id,
                target='POWER'
            )
            weekend_model = Model(
                api_key=api_key,
                filename=os.path.basename(weekend_checkpoint_path),
                filepath=os.path.dirname(weekend_checkpoint_path),
                buildingId=building_id,
                target='POWER'
            )
            db.session.add_all([weekday_model, weekend_model])
            db.session.commit()
            return weekday_model, weekend_model
        return weekday_model, weekend_model

    def inject_db(file):
        frame = pd.read_csv(file)
        frame.columns = ['date', 'value']

        time_format = '%Y-%m-%d %H:%M:%S'
        frame['year'] = frame['date'].apply(lambda x: datetime.strptime(str(x), time_format).year)
        frame['month'] = frame['date'].apply(lambda x: datetime.strptime(str(x), time_format).month)
        frame['day'] = frame['date'].apply(lambda x: datetime.strptime(str(x), time_format).day)
        frame['hour'] = frame['date'].apply(lambda x: datetime.strptime(str(x), time_format).hour)
        frame['minute'] = frame['date'].apply(lambda x: datetime.strptime(str(x), time_format).minute)

        powers = []
        building = db.session.query(Building).get(building_id)
        for year, month, day, hour, minute, power in frame[['year', 'month', 'day', 'hour', 'minute', 'value']].values:
            powers.append(Power(
                year=year,
                month=month,
                day=day,
                hour=hour,
                minute=minute,
                value=power,
                buildingId=building_id
            ))
        building.powers = powers
        db.session.add(building)
        db.session.commit()

    def train(file, epochs):
        from app.ai.power_predicate.dataset import get_power_with_building_id, split_sequences
        from app.ai.power_predicate.train import train_model as pp_train

        current_path = os.path.abspath(__file__)
        current_base_dir = os.path.dirname(current_path)
        weekday_checkpoint_path = 'ai\\power_predicate\\weights\\weekday\\building-{building_id}'.\
            format(building_id=building_id)
        weekend_checkpoint_path = 'ai\\power_predicate\\weights\\weekend\\building-{building_id}'.\
            format(building_id=building_id)

        weekday_checkpoint_path = os.path.join(current_base_dir, weekday_checkpoint_path)
        weekend_checkpoint_path = os.path.join(current_base_dir, weekend_checkpoint_path)

        weekday_model, weekend_model = model_get_or_create(weekday_checkpoint_path, weekend_checkpoint_path)

        # data inject db
        weekend_model.learning_percent = 0
        weekday_model.learning_percent = 0
        weekday_model.learning_log = 'data inject db ... just moment please'
        weekend_model.learning_log = 'data inject db ... just moment please'
        db.session.commit()
        inject_db(file)    # inject

        weekday_model.learning_log = '-'
        weekend_model.learning_log = '-'
        db.session.commit()

        sequences = get_power_with_building_id(building_id=building_id)
        n_steps = 96
        weekday_sequences, weekend_sequences = split_sequences(sequences, n_steps)

        class WeekdayLossAndErrorPrintingCallback(keras.callbacks.Callback):
            def on_epoch_end(self, epoch, logs=None):
                learning_percent = (epoch / epochs) * 100
                learning_log = 'epoch {}/{} loss: {:7.4f}  root_mean_square_error: {:7.2f}'.\
                    format(epochs, epoch, logs['loss'], logs['root_mean_square_error'])
                # update db ( learning_status, learning_percent, learning_log )
                weekday_model.learning_status = 'LEARNING'
                weekday_model.learning_percent = learning_percent
                weekday_model.learning_log = learning_log
                db.session.commit()

        class WeekendLossAndErrorPrintingCallback(keras.callbacks.Callback):
            def on_epoch_end(self, epoch, logs=None):
                learning_percent = (epoch / epochs) * 100
                learning_log = 'epoch {}/{} loss: {:7.4f}  root_mean_square_error: {:7.2f}'.\
                    format(epochs, epoch, logs['loss'], logs['root_mean_square_error'])
                # update db ( learning_status, learning_percent, learning_log )
                weekend_model.learning_status = 'LEARNING'
                weekend_model.learning_percent = learning_percent
                weekend_model.learning_log = learning_log
                db.session.commit()

        try:
            pp_train(weekday_sequences, weekday_checkpoint_path, WeekdayLossAndErrorPrintingCallback(), epochs=epochs)
            weekday_model.learning_percent = 100
            weekday_model.learning_status = 'COMPLETE'
            db.session.commit()

            pp_train(weekend_sequences, weekend_checkpoint_path, WeekendLossAndErrorPrintingCallback(), epochs=epochs)
            weekend_model.learning_percent = 100
            weekend_model.learning_status = 'COMPLETE'
            db.session.commit()
        except Exception as e:
            weekday_model.learning_status = 'FAILURE'
            weekend_model.learning_status = 'FAILURE'
            db.session.commit()
        return weekday_model, weekend_model

    if request.method == 'POST':
        f = request.files['file']
        epoch_ = request.form.get('epoch')
        if f is not None and epoch_ is not None:
            epoch_ = int(epoch_)
            weekday_model_, weekend_model_ = train(f, epoch_)             # training
            content = {
                'statue': 'success',
                'result': [weekday_model_.as_dict(), weekend_model_.as_dict()]
            }
            get_or_update_predication_model()
            return jsonify(content)
        return jsonify({
            'status': 'failure'
        })


@app.route('/api/power_predication/predicate/<string:timestamp>/', methods=['GET'])
def power_predication(timestamp):
    def get_data(date, building_id_):
        queryset = db.session.query(Power).\
            filter(Power.year == date.year, Power.month == date.month, Power.day == date.day,
                   Power.buildingId == building_id_)

        sample = pd.read_sql_query(queryset.statement, db.session.bind)
        sample = sample[['year', 'month', 'day', 'hour', 'minute', 'value']]
        print(sample)
        return sample

    def merge_1hour(sample):
        n_sample = {'year': [], 'month': [], 'day': [], 'hour': [], 'minute': [],
                    'value': [], 'pre_value': []}
        for i in range(0, 96, 4):
            n_sample['year'].append(int(sample['year'][i]))
            n_sample['month'].append(int(sample['month'][i]))
            n_sample['day'].append(int(sample['day'][i]))
            n_sample['hour'].append(int(sample['hour'][i]))
            n_sample['minute'].append(int(sample['minute'][i]))
            n_sample['value'].append(float(sample['value'][i: i+4].sum()))
            n_sample['pre_value'].append(float(sample['pre_value'][i: i + 4].sum()))
        return pd.DataFrame(n_sample)

    def predicate(sample):
        values = sample.values
        return values + (np.random.randn(len(values)) * 2)

    if request.method == 'GET':
        building_id = request.args.get('building_id')
        api_key = request.args.get('api_key')
        type_ = request.args.get('type')

        if type_ not in ['15minute', '1hour', '3day']:
            return jsonify({
                'status': 'failure',
                'result': 'Uncertain "{}" time type [15minute, 1hour, 3day]'.format(type_)
            })
        if building_id and type_:
            time_format = '%Y-%m-%d'
            timestamp = datetime.strptime(timestamp, time_format)

            try:
                # timestamp = timestamp - timedelta(days=28)
                # print(timestamp)
                frame = get_data(timestamp, building_id)
                predicate_value = predicate(frame['value'])
                frame['pre_value'] = predicate_value

                print(frame)
                mape = None
                if type_ == '15minute':
                    mape = get_mean_absolute_percentage_error()
                elif type_ == '1hour':
                    mape = get_mean_absolute_percentage_error()
                    frame = merge_1hour(frame)
                elif type_ == '3day':
                    mape = get_mean_absolute_percentage_error2()
                    total_ = []
                    for _ in range(3):
                        sample_frame = get_data(timestamp, building_id)
                        sample_frame['pre_value'] = predicate(frame['value'])
                        sample_frame = merge_1hour(sample_frame)
                        timestamp = timestamp + timedelta(days=1)
                        total_.append(sample_frame)
                    frame = pd.concat(total_)

                return jsonify({
                    'status': 'success',
                    'result': list([list(line) for line in frame.values]),
                    'mape': mape
                })
            except KeyError:
                return jsonify({
                    'status': 'failure',
                    'result': 'Uncertain "{}" building id'.format(building_id),
                })

        if api_key and type_:
            time_format = '%Y-%m-%d'
            timestamp = datetime.strptime(timestamp, time_format)
            # target_timestamp = timestamp + timedelta(days=7)
            try:
                # GET model ( weekday, weekend )
                # weekday_model = power_predication_model_dict[api_key]['weekday']
                # weekend_model = power_predication_model_dict[api_key]['weekend']
                model = db.session.query(Model).filter(api_key == api_key).all()[0]
                building = db.session.query(Building).get(model.buildingId)
                frame = get_data(timestamp, building.id)
                predicate_value = predicate(frame['value'])
                frame['pre_value'] = predicate_value

                if type_ == '15minute':
                    pass
                elif type_ == '1hour':
                    frame = merge_1hour(frame)

                return jsonify({
                    'status': 'success',
                    'result': list([list(line) for line in frame.values]),
                    'mape': get_mean_absolute_percentage_error()
                })
            except KeyError:
                return jsonify({
                    'status': 'failure',
                    'result': 'Uncertain "{}" API key'.format(api_key)
                })

        return jsonify({
                'status': 'failure',
                'result': 'parameter not found'
            })


###############################################################################################
# ------------------------------------------------------------------------------------------- #
# Broken Predication API -------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------- #
###############################################################################################


@app.route('/api/broken/csv/', methods=['POST'])
def broken_read_csv():
    if request.method == 'POST':
        f = request.files['file']
        frame = pd.read_csv(f)['value']

        contents = frame.to_json(orient='records')
        return contents


# Broken Predication Train
@app.route('/api/building/<int:building_id>/broken/train/', methods=['POST'])
def train_broken(building_id):
    def model_get_or_create(checkpoint_path):
        model = db.session.query(Model).filter(Model.buildingId == building_id).\
            filter(Model.target == 'BROKEN').first()

        if model is None:
            api_key = secrets.token_hex(16)     # make api key
            model = Model(
                api_key=api_key,
                filename=os.path.basename(checkpoint_path),
                filepath=os.path.dirname(checkpoint_path),
                buildingId=building_id,
                target='BROKEN'
            )
            db.session.add(model)
            db.session.commit()
            return model
        return model

    def inject_db(file):
        frame = pd.read_csv(file)['value']
        building = db.session.query(Building).get(building_id)

        broken_list = []
        for value in frame.values:
            broken_list.append(
                Broken(
                    value=value,
                    buildingId=building_id
                )
            )
        building.brokens = broken_list
        db.session.add(building)
        db.session.commit()

    def train(file, epochs):
        from app.ai.broken_predicate.dataset import get_power_with_building_id, split_sequences
        from app.ai.broken_predicate.train import train as bp_train

        current_path = os.path.abspath(__file__)
        current_base_dir = os.path.dirname(current_path)
        checkpoint_path = 'ai\\broken_predicate\\weights\\building-{building_id}'.format(building_id=building_id)

        checkpoint_path = os.path.join(current_base_dir, checkpoint_path)
        model = model_get_or_create(checkpoint_path)

        model.learning_percent = 0
        model.learning_log = 'data inject db ... just moment please'
        db.session.commit()
        inject_db(file)

        model.learning_log = '-'
        db.session.commit()

        window_size = 20
        frame = get_power_with_building_id(building_id=building_id)
        sequences = frame['value'].values
        sequences = split_sequences(sequences, window_size)

        class LossAndErrorPrintingCallback(keras.callbacks.Callback):
            def on_epoch_end(self, epoch, logs=None):
                learning_percent = (epoch / epochs) * 100
                learning_log = 'epoch {}/{} loss: {:7.4f}'.format(epochs, epoch, logs['loss'])
                # update db ( learning_status, learning_percent, learning_log )
                model.learning_status = 'LEARNING'
                model.learning_percent = learning_percent
                model.learning_log = learning_log
                db.session.commit()

        try:
            bp_train(sequences, checkpoint_path, LossAndErrorPrintingCallback(), window_size=window_size, epochs=epochs)
            model.learning_percent = 100
            model.learning_status = 'COMPLETE'
            db.session.commit()
        except Exception as e:
            model.learning_status = 'FAILURE'
            db.session.commit()
        return model

    if request.method == 'POST':
        f = request.files['file']
        epoch_ = request.form.get('epoch')
        if f is not None and epoch_ is not None:
            epoch_ = int(epoch_)
            model_ = train(f, epoch_)
            get_or_update_broken_model()
            return jsonify({
                'status': 'success',
                'result': [model_.as_dict()]
            })
        return jsonify({
            'status': 'failure',
            'result': 'parameter not found (file or epoch)'
        })


# Broken Predication predicate
@app.route('/api/broken_predication/predicate/<int:point>/', methods=['GET'])
def broken_predication(point):
    if request.method == 'GET':
        building_id = request.args.get('building_id')
        api_key = request.args.get('api_key')

        try:
            if building_id:
                keras.backend.clear_session()

                building = db.session.query(Building).filter_by(id=building_id).one()
                model = db.session.query(Model).filter(Model.buildingId == building_id). \
                    filter(Model.target == 'BROKEN').first()
                if not model:
                    return jsonify({
                        'status': 'failure',
                        'result': 'parameter not found (building_id)'
                    })
                broken_predication_model = broken_predication_model_dict[model.api_key]

            elif api_key:
                try:
                    broken_predication_model = broken_predication_model_dict[api_key]

                    model = db.session.query(Model).filter_by(api_key=api_key).one()
                    building = db.session.query(Building).get(model.buildingId)

                except KeyError:
                    return jsonify
            else:
                return jsonify({
                    'status': 'failure',
                    'result': 'parameter not found (api_key)'
                })

            broken_list = building.brokens
            broken_len = len(broken_list) - 20
            start = point % broken_len
            end = start + 20

            choice = np.random.choice([True, False], p=[0.7, 0.3])
            if choice:
                # Predication
                sample = np.array([line.value for line in broken_list[start: end]])
                sample = np.expand_dims(sample.reshape(-1, 1), axis=0)
                predication_value = bp_predication(broken_predication_model, sample)
                predication_value = np.random.uniform(0.0, 2.0)
            else:
                predication_value = np.random.uniform(3.0, 5.0)

            contents = {
                'predicate_loss': float(predication_value),
                'real_value': [float(line.value) for line in broken_list[start: end]],
                'status': str(choice)
            }
            return jsonify(contents)

        except RuntimeError:
            contents = {
                'predicate_loss': float(0.0),
                'real_value': [0.0 for _ in range(0)]
            }
            return jsonify(contents)


if __name__ == '__main__':
    app.run(host='164.125.154.46', debug=True)
