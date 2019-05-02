# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from tensorflow.python import keras
from tensorflow.python.keras.layers import Conv1D, MaxPooling1D, Dense, Flatten


def get_model_with_conv1d(inputs: keras.Input, filters: int, kernel_size: int):
    x = Conv1D(filters=filters, kernel_size=kernel_size, activation='relu')(inputs)
    x = MaxPooling1D(pool_size=2)(x)
    x = Flatten()(x)
    x = Dense(100)(x)
    outputs = Dense(96, name='outputs')(x)
    model = keras.Model(inputs=inputs, outputs=outputs, name='power predicate CNN model')
    return model

