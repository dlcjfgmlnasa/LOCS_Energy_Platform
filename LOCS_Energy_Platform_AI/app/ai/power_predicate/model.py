# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf
from tensorflow.python import keras
from tensorflow.python.keras.layers import Conv1D, MaxPooling1D, Dense, Flatten, BatchNormalization


def conv1d(inputs: keras.Input, filters: int, kernel_size: int):
    conv_1 = Conv1D(filters=filters, kernel_size=kernel_size, activation=keras.activations.relu)(inputs)
    conv_1 = MaxPooling1D(pool_size=2)(conv_1)
    flat = Flatten()(conv_1)
    fc_1 = Dense(128, activation=keras.activations.relu)(flat)
    fc_1 = BatchNormalization()(fc_1)
    outputs = Dense(1, name='output_layer', dtype=tf.float32)(fc_1)

    model = keras.Model(inputs=inputs, outputs=outputs)
    return model
