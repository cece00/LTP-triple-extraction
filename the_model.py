from keras.layers import Dense, Flatten, Dropout
from keras.layers import Conv1D, MaxPooling1D, Embedding
from keras.models import Sequential
import pre_model as pre
import numpy as np


model = Sequential()
model.add(Embedding(len(pre.word_index) + 1, pre.EMBEDDING_DIM, input_length=pre.MAX_SEQUENCE_LENGTH))
model.add(Dropout(0.2))
model.add(Conv1D(250, 3, padding='valid', activation='relu', strides=1))  # 输出250
model.add(MaxPooling1D(3))   # 池化窗口3
model.add(Flatten())   # 一维化
model.add(Dense(pre.EMBEDDING_DIM, activation='relu'))
model.add(Dense(pre.labels.shape[1], activation='softmax'))
# print(pre.labels.shape[1])   50
model.summary()

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(pre.x_train, pre.y_train, validation_data=(pre.x_val, pre.y_val), epochs=1, batch_size=128)
eval = model.evaluate(pre.x_test, pre.y_test)
print(eval)

# save model

print("Saving model to disk \n")
mp = "./model/spo_model.h5"
with open(mp):
	model.save(mp)


# for i in range(0, 100):
#     print(pre.D.the_text[i])
#     print(predicate[i])
#     print(the_predicate[i])
#     print(pre.labels[i])

# print(pre.data[0],type(pre.data),type(pre.data[0]))  # 都是ndarray
# print(pre.x_test[0],pre.y_test[0],type(pre.x_test),type(pre.y_test))
