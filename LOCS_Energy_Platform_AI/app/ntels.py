# -*- coding:utf-8 -*-
import asyncio
import requests
import datetime
import pandas as pd
import app.server as server
import app.tables as models

db = server.db
base_url = 'https://nisbcp.ntels.com:18080'
time_format = '%Y%m%d%H%M%S'


def login():
    login_url = base_url + '/NISBCP/login/doLogin.do'
    login_params = dict(
        user_id='nisbcp',
        user_pw='nisbcp'
    )
    with requests.Session() as sess:
        try:
            sess.post(login_url, login_params, verify=False, allow_redirects=True, timeout=90)
            return sess
        except requests.exceptions.ConnectionError:
            raise ConnectionError('Could not login to server, check server configuration..')


def get_datetime_date(time_frame):
    values = [datetime.datetime.strptime(value, time_format) for value in time_frame.values]
    temp = []
    for value in values:
        temp.append({
            'year': value.year,
            'month': value.month,
            'day': value.day,
            'hour': value.hour,
            'minute': value.minute,
        })
    return pd.DataFrame(temp)


def get_data(login_session, building, start_date, end_date):
    url = '{0}/NISBCP/urbanmap/energy/getBuildingEnergyTrend.ajax?startDate={1}&endDate={2}&bid={3}&period={4}'. \
        format(base_url, start_date, end_date, building.as_dict()['bld'], '15m')
    try:
        columns = ['logdate', 'usage']
        response = login_session.get(url, verify=False, timeout=90)
        contents = response.json()

        if contents['empty']:
            raise IndexError('Empty data List')
        frame = pd.DataFrame(contents['list'])[columns]
        n_frame = get_datetime_date(frame[columns[0]])
        n_frame['Power'] = frame[columns[1]]
        return n_frame
    except ConnectionError:
        raise ConnectionError('Could not get data from https request, check server API configuration')


def export_power_data(building, frame):
    powers = []
    for year, month, day, hour, minute, power in frame[['year', 'month', 'day', 'hour', 'minute', 'Power']].values:
        powers.append(models.Power(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=month,
            value=power))
    building.powers = powers
    return building


async def export_data(login_session, building, start_date, end_date):
    print('building %s data export to db' % building.as_dict()['name'])
    try:
        frame = get_data(login_session, building, start_date, end_date)
        building = export_power_data(building, frame)
        db.session.add(building)
        db.session.commit()
    except IndexError:
        print('error')


async def async_bulk(start_date, end_date):
    login_session = login()
    futures = []
    for building in db.session.query(models.Building).all():
        futures.append(export_data(login_session, building, start_date, end_date))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(futures))
    

def bulk(start_date, end_date):
    login_session = login()

    for building in db.session.query(models.Building).all():
        print('building %s data export to db' % building.as_dict()['name'])

        frame = get_data(login_session, building, start_date, end_date)
        building = export_power_data(building, frame)
        db.session.add(building)
        db.session.commit()


bulk('20181130234500', '20190417234500')


