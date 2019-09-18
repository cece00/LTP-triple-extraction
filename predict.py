# 模型的加载及使用
from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
import pre_model as pre
import numpy as np
import deal_data as D
import re

MAX_SEQUENCE_LENGTH = 100  # 每条语料最大长度
EMBEDDING_DIM = 200  # 词向量空间维度

def label2schema(label_array):
	with open('../data/all_50_schemas', 'r', encoding='UTF-8') as lf:
		i = 0
		label_dic = dict()
		for line in lf:
			pattern = "object_type\": \"(.*?)\", \"predicate\": \"(.*?)\", \"subject_type\": \"(.*?)\""
			temp = re.findall(pattern, line)
			t = [temp[0][0],temp[0][1],temp[0][2]]
			label_dic[i] = t
			i += 1

		str_predicate = []
		for item in label_array:
			str_predicate.append(label_dic[item])

	return str_predicate


the_text = []
with open('../finalymtan/test_segspo_ymtan.txt','r',encoding='utf-8') as tssf:
	for line in tssf.readlines():
		line = D.clearSen(line)
		line = line.strip('\n')
		the_text.append(line)
tssf.close()


# tokenizer = Tokenizer(num_words=50040)  # 向量化文本，或将文本转换为序列的类
# tokenizer.fit_on_texts(the_text)

print("Using loaded model to predict...")
model = load_model("./model/spo_model.h5")
tokenizer = pre.tokenizer
sequences = tokenizer.texts_to_sequences(the_text)  # 将一个句子拆分成单词构成的列表
word_index = tokenizer.word_index  # 一个dict，保存所有word对应的编号id，从1开始
# print(word_index)
print('Found unique tokens:', len(word_index))
data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)
print('Shape of data tensor:', data.shape)

predicate = model.predict(data)
# print(predicate[0])
# print(predicate)
np_predicate = np.array(predicate)
# print(np_predicate[1])
the_predicate = []
for i in range(len(the_text)):
	the_predicate.append(np.argmax(np_predicate[i]))

print(the_predicate)
print(len(the_predicate))

str_predicate = label2schema(the_predicate)#得到了label对应的o_type，predicate和s_type,一个list套list


with open("../finalymtan/5_spo.txt",'a',encoding='utf-8') as spof:
	for i in range(len(str_predicate)):
		if i%200 == 0:
			
		t = the_text[i].split(' ')
		spof.write(t[-3])
		spof.write(' ')
		spof.write(t[-1])
		spof.write(' ')
		spof.write(" ".join(str_predicate[i]))
		spof.write('\n')
#subject,object,o_type,predicate,s_type
spof.close()


