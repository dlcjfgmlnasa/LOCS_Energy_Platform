# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function
import tensorflow as tf
from tensorflow.python.keras.models import Model
from tensorflow.python.keras.layers import Dense, Flatten, Conv2D


class PowerPredicateWithLSTM(Model):
    def __init__(self):
        super(Model, self).__init__()

