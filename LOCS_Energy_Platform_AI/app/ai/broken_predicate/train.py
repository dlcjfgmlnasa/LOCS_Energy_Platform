# -*- coding:utf-8 -*-
import os
from app.ai.broken_predicate.model import conv1d_autoencoder
from tensorflow.python import keras


def train(
        sequences,
        checkpoint_path,
        cp_checkpoint,
        window_size=100,
        filters=128,
        kernel_size=5,
        units=64,
        epochs=20,
        batch_size=50,
        validation_split=0.2):
    n_features = 1

    # make model
    inputs = keras.Input(shape=(window_size, n_features), name='input_layer')
    model = conv1d_autoencoder(
        inputs,
        filters=filters,
        kernel_size=kernel_size,
        units=units,
        windows_size=window_size
    )
    if os.path.exists(checkpoint_path):
        model.load_weights(checkpoint_path)

    model.summary()
    model.compile(
        optimizer=keras.optimizers.Adam(),
        loss=keras.losses.mean_squared_error
    )

    # Training
    model.fit(
        x=sequences[0],
        y=sequences[1],
        batch_size=batch_size,
        epochs=epochs,
        verbose=1,
        validation_split=validation_split,
        callbacks=[
            cp_checkpoint
        ],
    )
    model.save_weights(checkpoint_path)
