import scipy.io as sio
import numpy as np
import keras
from keras.callbacks import EarlyStopping
from keras import Sequential
from keras.layers import Dense, Flatten, Conv2D, MaxPooling2D
from keras.utils import to_categorical
import matplotlib.pyplot as plt

# Main Code
# Load the Data
path = ''
trainims, trainlbls = sio.loadmat(path + 'trainims'), sio.loadmat(path + 'trainlbls')
trainims, trainlbls = trainims['images'], trainlbls['labels']
testims, testlbls = sio.loadmat(path + 'testims'), sio.loadmat(path + 'testlbls')
testims, testlbls = testims['images'], testlbls['labels']
(numOfTraining, pixels) = trainims.shape
trainims = np.reshape(trainims,(numOfTraining,28,28,1))
(numOfTest, pixels) = testims.shape
testims = np.reshape(testims,(numOfTest,28,28,1))
trainlbls, testlbls = to_categorical(trainlbls), to_categorical(testlbls)
trainlbls, testlbls = trainlbls[:,1:], testlbls[:,1:]

# numOfTraining = 124800, numOfTest = 20800

model = Sequential()
model.add(Conv2D(32,(3,3), input_shape = (28,28,1), activation = 'relu'))
model.add(MaxPooling2D(pool_size = (2, 2)))
model.add(Flatten())
model.add(Dense(units= 64, activation='relu'))
model.add(Dense(units = 26, activation='softmax'))
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(trainims, trainlbls, epochs = 6, batch_size=128, validation_split=0.1)

model_json = model.to_json()
with open("Letter.json", "w") as json_file:
    json_file.write(model_json)
model.save_weights("Letter.h5")
