from __future__ import print_function
from sklearn.cross_validation import train_test_split
import pandas as pd
import numpy as np
np.random.seed(1337)  # for reproducibility
from keras.preprocessing import sequence
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Embedding
from keras.layers import LSTM, SimpleRNN, GRU
from keras.datasets import imdb
from keras.utils.np_utils import to_categorical
from sklearn.metrics import (precision_score, recall_score,
                             f1_score, accuracy_score,mean_squared_error,mean_absolute_error)
from sklearn import metrics
from sklearn.preprocessing import Normalizer
import h5py
from keras import callbacks
from keras import callbacks
from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau, CSVLogger
from keras.layers import recurrent
from keras.initializations import normal, identity
from keras.optimizers import RMSprop

traindata = pd.read_csv('kdd/multiclass/train.csv', header=None)
testdata = pd.read_csv('kdd/multiclass/test.csv', header=None)


X = traindata.iloc[:,0:22]
Y = traindata.iloc[:,22]
C = testdata.iloc[:,22]
T = testdata.iloc[:,0:22]



scaler = Normalizer().fit(X)
trainX = scaler.transform(X)
# summarize transformed data
np.set_printoptions(precision=3)
#print(trainX[0:5,:])

scaler = Normalizer().fit(T)
testT = scaler.transform(T)
# summarize transformed data
np.set_printoptions(precision=3)
#print(testT[0:5,:])

y_train1 = np.array(Y)
y_test1 = np.array(C)

y_train= to_categorical(y_train1)
y_test= to_categorical(y_test1)



# reshape input to be [samples, time steps, features]
X_train = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
X_test = np.reshape(testT, (testT.shape[0], 1, testT.shape[1]))


batch_size = 64
learning_rate = 0.1

# 1. define the network
model = Sequential()
model.add(SimpleRNN(64,init=lambda shape, name: normal(shape, scale=0.001, name=name),inner_init=lambda shape, name: identity(shape, scale=1.0, name=name),input_dim=22,activation='relu',return_sequences=True))  # try using a GRU instead, for fun
model.add(SimpleRNN(64,activation='relu',return_sequences=True))
model.add(SimpleRNN(64,activation='relu',return_sequences=True))
model.add(SimpleRNN(64,activation='relu',return_sequences=True))
model.add(SimpleRNN(64,activation='relu',return_sequences=True))
model.add(SimpleRNN(64,activation='relu',return_sequences=True))
model.add(SimpleRNN(64,activation='relu',return_sequences=True))
model.add(SimpleRNN(64,activation='relu',return_sequences=False))
model.add(Dense(11))
model.add(Activation('softmax'))
rmsprop = RMSprop(lr=learning_rate)


# try using different optimizers and different optimizer configs
model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
checkpointer = callbacks.ModelCheckpoint(filepath="kddresults/lstm8layer/checkpoint-{epoch:02d}.hdf5", verbose=1, save_best_only=True, monitor='val_acc',mode='max')
csv_logger = CSVLogger('training_set_iranalysis8.csv',separator=',', append=False)
model.fit(X_train, y_train, batch_size=batch_size, nb_epoch=1000, validation_data=(X_test, y_test),callbacks=[checkpointer,csv_logger])
model.save("kddresults/lstm8layer/lstm1layer_model.hdf5")

loss, accuracy = model.evaluate(X_test, y_test)
print("\nLoss: %.2f, Accuracy: %.2f%%" % (loss, accuracy*100))
y_pred = model.predict_classes(X_test)
np.savetxt('kddresults/lstm8layer/lstm1predicted.txt', np.transpose([y_test1,y_pred]), fmt='%01d')








