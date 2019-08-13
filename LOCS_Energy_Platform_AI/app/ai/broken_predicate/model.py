# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from tensorflow.python import keras
from tensorflow.python.keras.layers import LSTM, Conv1D, Dense, BatchNormalization


def conv1d_autoencoder(
        inputs: keras.Input,
        filters: int,
        kernel_size: int,
        units: int,
        windows_size: int
    ):
    # CNN + LSTM AutoEncoder
    conv = Conv1D(filters=filters, kernel_size=kernel_size, padding='same',
                  activation=keras.activations.relu)(inputs)
    rnn = LSTM(units=units)(conv)
    rnn = BatchNormalization()(rnn)
    outputs = Dense(units=windows_size, activation='linear')(rnn)
    model = keras.Model(inputs=inputs, outputs=outputs)
    return model
