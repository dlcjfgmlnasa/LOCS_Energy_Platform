# -*- coding:utf-8 -*-
import os
import datetime
import pandas as pd

path = 'app\\ai\\power_predicate\\power_dataset'
filename = 'B0051.csv'

frame = pd.read_csv(os.path.join(path, filename))
columns = frame.columns
