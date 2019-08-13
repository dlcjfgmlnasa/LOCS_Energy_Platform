# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import os
import argparse
import numpy as np
from tensorflow.python import keras
from app.ai.broken_predicate.model import conv1d_autoencoder


keras.backend.set_learning_phase(0)     # Ignore dropout at inference


def get_args():
    parser = argparse.ArgumentParser(description='Train broken predicate')
    parser.add_argument('--units', default=64,
                        help='lstm units size (default:64)')
    parser.add_argument('--filters', default=128,
                        help='cnn filter size (default:128)')
    parser.add_argument('--kernel_size', default=5,
                        help='cnn kernel size (default:5)')
    parser.add_argument('--window_size', default=20,
                        help='windows size (default:20)')
    parser.add_argument('--weight_path', default='./weights/my_model',
                        help='weight path')
    args = parser.parse_args()
    return args


def get_model(file_path: str, file_name: str):
    args = get_args()
    n_feature = 1

    inputs = keras.Input(shape=(args.window_size, n_feature), name='input_layer')
    model = conv1d_autoencoder(
        inputs,
        filters=args.filters,
        kernel_size=args.kernel_size,
        units=args.units,
        windows_size=args.window_size
    )
    file_path = os.path.join(file_path, file_name)
    model.load_weights(file_path)
    return model


def predication(model: keras.Model, sample: np.array):
    sample = model.predict(sample)[0]
    predication_value = np.sum(np.abs(sample)) / len(sample)
    return predication_value


