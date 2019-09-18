from keras.layers import Dense, Flatten, Dropout
from keras.layers import Conv1D, MaxPooling1D, Embedding,LSTM,Bidirectional
from keras.models import Sequential
import pre_model as pre
import numpy as np


model = Sequential()
model.add(Embedding(len(pre.word_index) + 1, pre.EMBEDDING_DIM, input_length=pre.MAX_SEQUENCE_LENGTH))
model.add(Dropout(0.2))
model.add(Bidirectional(LSTM(pre.lstm_out, dropout_U =0.2, dropout_W =0.2, return_sequences=True),merge_mode = 'concat'))

model.add(Flatten())   # 一维化
model.add(Dense(pre.EMBEDDING_DIM, activation='relu'))
model.add(Dense(pre.labels.shape[1], activation='softmax'))
model.summary()

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(pre.x_train, pre.y_train, validation_data=(pre.x_val, pre.y_val), epochs=1, batch_size=128)
eval = model.evaluate(pre.x_test, pre.y_test)
print(eval)

# save model

print("Saving model to disk \n")
mp = "./model/spo_lstm.h5"
with open(mp):
	model.save(mp)
