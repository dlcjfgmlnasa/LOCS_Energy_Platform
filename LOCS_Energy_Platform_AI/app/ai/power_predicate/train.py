# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from tensorflow.python.keras import Input
from app.ai.power_predicate.model import get_model_with_conv1d
from app.ai.power_predicate.dataset import get_power_with_building_id, split_sequences


def example_plot(true, pred, ax):
    ax.plot(true)
    ax.plot(pred)


def root_mean_square_deviation(y_true, y_pred):
    return tf.sqrt(tf.reduce_mean(tf.square(tf.subtract(y_true, y_pred))))


def train_with_convolution_neural_network(
        building_id: int,
        filters: int,
        kernel_size: int,
        split_rate: float,
        epoch=1000,
        batch_size=20
    ):
    n_steps_in, n_steps_out = 96, 96
    # Get power Dataset
    sequences = get_power_with_building_id(building_id)

    # Split Dataset
    split_index = int(len(sequences) * (1 - split_rate))
    train_data, test_data = sequences[:split_index], sequences[split_index:]

    # Split sequences
    train_x, train_y = split_sequences(train_data, n_steps_in, n_steps_out)
    test_x, test_y = split_sequences(test_data, n_steps_in, n_steps_out)

    # Train
    inputs = Input(shape=(train_x.shape[1], train_x.shape[2]), name='inputs')
    model = get_model_with_conv1d(inputs, filters=filters, kernel_size=kernel_size)
    model.summary()
    model.compile(optimizer='adam', loss='mse', metrics=[root_mean_square_deviation])
    model.fit(train_x, train_y,
              validation_data=(test_x, test_y),
              epochs=epoch,
              batch_size=batch_size,
              verbose=0)

    # Test
    test_loss, test_acc = model.evaluate(test_x, test_y)
    print('Test Loss : {0} / Test RMSE : {1}'.format(test_loss, test_acc))

    # Show Image
    fig, axes = plt.subplots(nrows=5, ncols=5)
    rands = np.random.randint(0, len(test_x), 25)
    i = 0
    for row in axes:
        for each_ax in row:
            random_number = rands[i]
            pred = model.predict(test_x[random_number][np.newaxis, :])[0]
            true = test_y[i]
            example_plot(true, pred, each_ax)
            i = i+1
    plt.tight_layout()
    plt.show()


train_with_convolution_neural_network(1, 64, 2, 0.1)

