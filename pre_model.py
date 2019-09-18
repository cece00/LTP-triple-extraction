#coding:utf-8
# from __future__ import print_function
# from __future__ import unicode_literals

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
import numpy as np
import deal_data as D
import get_label as get


MAX_SEQUENCE_LENGTH = 100  # 每条语料最大长度
EMBEDDING_DIM = 200  # 词向量空间维度
lstm_out =128
VALIDATION_SPLIT = 0.16  # 验证集比例
TEST_SPLIT = 0.2  # 测试集比例

# print(D.get_data)
# fenci_data = list(D.tr_text)

tokenizer = Tokenizer(num_words=50040)  # 向量化文本，或将文本转换为序列的类
tokenizer.fit_on_texts(D.the_text)
sequences = tokenizer.texts_to_sequences(D.the_text)  # 将一个句子拆分成单词构成的列表
# print(D.the_text[0])

word_index = tokenizer.word_index  # 一个dict，保存所有word对应的编号id，从1开始
# print(word_index)
print('Found unique tokens:', len(word_index))
data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)
# print(data[0])
labels = to_categorical(np.asarray(get.label))
print("labels:",labels)
# print(labels[0])
# print(len(data))
print('Shape of data tensor:', data.shape)
print('Shape of label tensor:', labels.shape)

p1 = int(len(data)*(1-VALIDATION_SPLIT-TEST_SPLIT))
# print(p1, type(p1))    # 6399 int
p2 = int(len(data)*(1-TEST_SPLIT))
x_train = data[:p1]
# print(x_train.shape)
y_train = labels[:p1]
# y_train = Flatten()(y_train)
# print(y_train)  # 63 50 2
x_val = data[p1:p2]
y_val = labels[p1:p2]
x_test = data[p2:]
y_test = labels[p2:]
print('train docs: ', len(x_train))
print('val docs: ', len(x_val))
print('test docs: ', len(x_test))
# print(data)