#!/usr/bin/env python

"order integer sequences of length given by n_steps"

import pickle
import numpy as np
import ast
import tensorflow as tf
from keras.models import Model
from keras.layers import LSTM, Input
from keras.utils.np_utils import to_categorical
from keras.layers import Embedding, TimeDistributed, Dense
from keras.preprocessing.sequence import pad_sequences
from keras.callbacks import ModelCheckpoint

from PointerLSTM import PointerLSTM

import cPickle as cpickle
#

n_steps = 10
embedding_dim = 100

f = open('data/vocab.txt', 'r')
vocab = f.read().rstrip('\n').split('\n')
f.close()

f1 = open('tokens/pred.txt', 'w')

x_train = cpickle.load(open("tokens/x_train.p", "rb" ))
y_train = cpickle.load(open("tokens/y_train.p", "rb" ))
x_test = cpickle.load(open("tokens/x_test.p", "rb" ))
y_test = cpickle.load(open("tokens/y_test.p", "rb" ))
x_val = cpickle.load(open("tokens/x_val.p", "rb" ))
y_val = cpickle.load(open("tokens/y_val.p", "rb" ))

# split_at = 9000
batch_size = 256

hidden_size = 100
weights_file = 'model_weights/mw_{}_steps_{}.hdf5'.format(n_steps, hidden_size)

x_train = np.array(x_train)
# x_train = pad_sequences(x_train, maxlen=40, padding='post')
x_train = np.expand_dims(x_train, axis=2)
x_test = np.array(x_test)
# x_test = pad_sequences(x_test, maxlen=40, padding='post')
x_test = np.expand_dims(x_test, axis=2)
x_val = np.array(x_val)
# x_val = pad_sequences(x_val, maxlen=40, padding='post')
x_val = np.expand_dims(x_val, axis=2)

print x_train.shape
print x_test.shape
print x_val.shape
# print y_train[1]
YY_train = []
YY_val = []
YY_test = []

for y_ in y_train:
    YY_train.append(to_categorical(y_))
for y_ in y_test:
    YY_test.append(to_categorical(y_))
for y_ in y_val:
    YY_val.append(to_categorical(y_))

YY_train = np.array(YY_train)
YY_test = np.array(YY_test)
YY_val = np.array(YY_val)

print 'Vectors loaded'
assert (n_steps == x_train.shape[1])
# x = np.expand_dims( x, axis = 2 )

# YY = []
# for y_ in y:
# 	YY.append(to_categorical(y_))
# YY = np.asarray(YY)

# x_train = x[:split_at]
# x_test = x[split_at:]
#
# y_test = y[split_at:]
# YY_train = YY[:split_at]
# YY_test = YY[split_at:]

# assert( n_steps == x.shape[1] )

print( "building model..." )
# with tf.device('/cpu:0'):
main_input = Input( shape=( n_steps, 1 ), name='main_input' )

encoder = LSTM(output_dim = hidden_size, return_sequences = True, name="encoder")(main_input)
decoder = PointerLSTM(hidden_size, output_dim=hidden_size, name="decoder")(encoder)

model = Model( input=main_input, output=decoder )

model.summary()
# print( "loading weights from {}...".format( weights_file ))
# try:
# 	model.load_weights(weights_file)
# except IOError:
# 	print( "no weights file, starting anew." )

model.compile(optimizer='rmsprop',
			  loss='categorical_crossentropy',
			  metrics=['accuracy'])

# print( 'training and saving model weights each epoch...' )

validation_data = (x_val, YY_val)
e = 0
while True:
    print 'Doing Epoch : ' + str(e+1)
    e+=1
    checkpoint = ModelCheckpoint(weights_file, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
    callbacks_list = [checkpoint]
    history = model.fit(x_train, YY_train, nb_epoch = 1, verbose=1, batch_size = batch_size, validation_data = validation_data, callbacks = callbacks_list)
    p = model.predict(x_test)
    loss, acc = model.evaluate(x_test, YY_test, batch_size)
    print('Test loss / test accuracy = {:.4f} / {:.4f}'.format(loss, acc))
    f1 = open('tokens/pred.txt', 'w')
    for vals in p:
        f1.write(str(vals.argmax(axis=1))+'\n')
    i = 0
    for y_, p_ in zip( y_test, p )[:5]:
		print "y_test:", y_
		print "p:     ", p_.argmax( axis = 1 )
		print
    # for y_, p_ in list(zip(y_test, p))[:5]:
    #     print "y_test:", y_
    #     print "p:     ", p_.argmax(axis = 1)
    #     print
    #     i += 1
    #     if i==5:
    #         break
        # import keras.backend as K
        # K.clear_session()
    model.save('model')
