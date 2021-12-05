# -*- coding: utf-8 -*-
"""My_First_RNN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Kh104CHfB2_Nbomw4hqV8oEw2R5t7QX5
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
import sklearn as sk
import tensorflow as tf
import tensorflow_hub as hub
from tensorflow import keras
import os
import pathlib
import cv2
import PIL.Image
# %load_ext tensorboard

time=np.arange(0, 50, 0.1)

amp=np.cos(time)

plt.figure(figsize=(12,8))
plt.plot(time, amp)
plt.xlabel("Time")
plt.ylabel("Amplitude")

len(time) == len(amp)

data=pd.DataFrame(amp, index=time, columns=["amp"])

0.8 * 500

train_data=data.iloc[:400]
test_data=data.iloc[400:]

plt.plot(test_data)

train_data.iloc[:25].plot()

"""FEATURE SCALING"""

from sklearn.preprocessing import MinMaxScaler

data=MinMaxScaler()
scaled_train=data.fit_transform(train_data)
scaled_test=data.transform(test_data)

"""TIME SERIES GENERATOR"""

from keras.preprocessing.sequence import TimeseriesGenerator

length=65

train_gen=TimeseriesGenerator(scaled_train, scaled_train, length=length, batch_size=2)
test_gen=TimeseriesGenerator(scaled_test, scaled_test, length=length, batch_size=2)

"""Build Model"""

from keras.layers import Dense, SimpleRNN, LSTM

model=tf.keras.models.Sequential()
model.add(LSTM(length, input_shape=(length, 1)))
model.add(Dense(1))
model.compile("adam", "mse")

"""Early Stopping"""

# from keras.callbacks import EarlyStopping, History
# stop=EarlyStopping(monitor="val_loss", mode="min")
# history=History()

model.fit(train_gen, epochs=8)

model.save("rnn_lstm_model.h5")

eval=np.expand_dims(scaled_train[-length:],0)

model.predict(eval)

scaled_test[0]

len(scaled_test)

test_predictions = []

first_eval_batch = scaled_train[-length:]
current_batch = np.expand_dims(scaled_train[-length:],0)

for i in range(len(scaled_test)):
    
    # get prediction 1 time stamp ahead ([0] is for grabbing just the number instead of [array])
    current_pred = model.predict(current_batch)[0]
    
    # store prediction
    test_predictions.append(current_pred) 
    
    # update batch to now include prediction and drop first value
    current_batch = np.append(current_batch[:,1:,:],[[current_pred]],axis=1)

pred=data.inverse_transform(test_predictions)

res=pd.DataFrame(test_data["amp"].values, columns=["real"])
res['pred']=pred

res.plot(figsize=(12,8))

"""__________<h1>FORECASTING </h1>______________"""

test_predictions = []

first_eval_batch = scaled_train[-length:]
current_batch = np.expand_dims(scaled_train[-length:],0)
forecast_upto=400

for i in range(forecast_upto):
    
    # get prediction 1 time stamp ahead ([0] is for grabbing just the number instead of [array])
    current_pred = model.predict(current_batch)[0]
    
    # store prediction
    test_predictions.append(current_pred) 
    
    # update batch to now include prediction and drop first value
    current_batch = np.append(current_batch[:,1:,:],[[current_pred]],axis=1)

pred=data.inverse_transform(test_predictions)

train_data.plot()

# REAL GRAPH

res=pd.DataFrame(pred).plot()

# FORECASTED GRAPH