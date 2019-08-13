# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import os
import argparse
import tensorflow as tf
from tensorflow.python import keras
from app.ai.power_predicate.model import conv1d
from app.ai.power_predicate.dataset import get_power_with_building_id, split_sequences, n_features


def get_args():
    parser = argparse.ArgumentParser(description='Train power prediction model')
    parser.add_argument('--building_id', default='1',
                        help='locs_eprophet power building id')
    parser.add_argument('--filters', default=64,
                        help='cnn filter size (default:64)')
    parser.add_argument('--kernel_size', default=20,
                        help='cnn kernel size (default:20)')
    parser.add_argument('--epochs', default=10,
                        help='Train epoch size (default:20)')
    parser.add_argument('--batch_size', default=50,
                        help='Train batch size (default:20)')
    parser.add_argument('--validation_split', default=0.2,
                        help='train data validation rate (default: 0.2)')
    return parser.parse_args()


def root_mean_square_error(y_true, y_pred):
    return tf.sqrt(tf.losses.mean_squared_error(y_true, y_pred))


class LossAndErrorPrintingCallback(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        print('\n')
        print('epoch {} loss: {:7.2f} root_mean_square_error: {:7.2f}'
              .format(epoch, epoch, logs['loss'], logs['root_mean_square_error']))


def train_model(
        sequences,
        checkpoint_path,
        cp_checkpoint,
        filters=64,
        kernel_size=20,
        epochs=10,
        batch_size=50,
        validation_split=0.2):

    n_steps = 96
    inputs = keras.Input(shape=(n_steps, n_features), name='input_layer')
    model = conv1d(
        inputs=inputs,
        filters=filters,
        kernel_size=kernel_size
    )

    if os.path.exists(checkpoint_path):
        model.load_weights(checkpoint_path)

    model.summary()
    model.compile(
        optimizer=keras.optimizers.Adam(),
        loss='mean_squared_error',
        metrics=[root_mean_square_error]
    )

    model.fit(
        x=sequences[0],
        y=sequences[1],
        epochs=epochs,
        batch_size=batch_size,
        validation_split=validation_split,
        use_multiprocessing=True,
        workers=4,
        callbacks=[
            # `val_loss`가 2번의 에포크에 걸쳐 향상되지 않으면 훈련을 멈춥니다.
            # keras.callbacks.EarlyStopping(patience=2, monitor='loss'),
            # `./logs` 디렉토리에 텐서보드 로그를 기록니다.
            # keras.callbacks.TensorBoard(log_dir='./logs')
            cp_checkpoint
        ],
    )

    model.save_weights(checkpoint_path)


def train():
    args = get_args()
    sequences = get_power_with_building_id(args.building_id)
    n_steps = 96
    weekday_sequences, weekend_sequences = split_sequences(sequences, n_steps)
    weekday_checkpoint_path = './weights/weekday/building-{building_id}'.format(building_id=args.building_id)
    weekend_checkpoint_path = './weights/weekend/building-{building_id}'.format(building_id=args.building_id)

    train_model(weekday_sequences, weekday_checkpoint_path, LossAndErrorPrintingCallback())
    train_model(weekend_sequences, weekend_checkpoint_path, LossAndErrorPrintingCallback())


if __name__ == '__main__':
    train()

