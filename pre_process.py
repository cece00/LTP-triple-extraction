import json
import codecs
import re
TR_SIZE = 0


class deal_data:
	def __init__(self):
		self.total = 0
		self.train_dict = []
		self.tr_text = []
		self.tr_postag = []
		self.tr_spo =[]

		with open("../data/train_data.json", 'rb+') as train_dataf:
			for lines in train_dataf:
				self.total += 1
				tr_data = json.loads(lines.decode())
				self.train_dict.append(tr_data)
				# if self.total == TR_SIZE:
				# 	break


		for i in range(self.total):
			self.tr_text.append(self.train_dict[i]['text'])
			self.tr_postag.append(self.train_dict[i]['postag'])  # tr_postag的每一项是一个list（由dict组成）
			self.tr_spo.append(self.train_dict[i]['spo_list'])

	def save_trainset(self):
		with open('./label.txt', 'w+', encoding='utf-8') as lf:
			for i in range(self.total):
				for j in range(len(self.tr_spo[i])):#多个三元组的情形
					lf.write(self.tr_spo[i][j]['predicate'])
					lf.write('\n')


		# 把文件里的object和subject按照object_type和subject_type分类
		for i in range(self.total):
			print(len(self.tr_spo[i]))


	'''
	segpos:
	[[['w1','w2',...]['pos1','pos2',...]]
	 [                   ...             ]  
	]
	'''
	#把百度标记好的词性转换换为ltp需要的词性
	def change_pos_build(self, mode):#mode = 0时修改pos
		segpos = []

		if mode == 0:
			i = 0
			for item in self.tr_postag:
				one_segpos = [[], []]
				for index in range(len(item)):#item[index]指的是{'pos': 'r', 'word': '如何'}
					if item[index]['pos'] == 'f':
						item[index]['pos'] = 'nl'
					elif item[index]['pos'] == 's':
						item[index]['pos'] = 'nd'
					elif item[index]['pos'] == 't':
						item[index]['pos'] = 'nt'
					elif item[index]['pos'] == 'nt':
						item[index]['pos'] = 'nl'
					elif item[index]['pos'] == 'nw':
						item[index]['pos'] = 'nz'
					elif item[index]['pos'] == 'vd' or item[index]['pos'] == 'vn' :
						item[index]['pos'] = 'v'
					elif item[index]['pos'] == 'ad' or item[index]['pos'] == 'an':
						item[index]['pos'] = 'a'
					elif item[index]['pos'] == 'xc':
						item[index]['pos'] = 'x'
					elif item[index]['pos'] == 'w':
						item[index]['pos'] = 'wp'
					one_segpos[0].append(item[index]['word'])
					one_segpos[1].append(item[index]['pos'])
				segpos.append(one_segpos)
		elif mode == 1:
			for item in self.tr_postag:
				one_segpos = [[], []]
				for index in range(len(item)):#item[index]指的是{'pos': 'r', 'word': '如何'}
					one_segpos[0].append(item[index]['word'])
					one_segpos[1].append(item[index]['pos'])

				segpos.append(one_segpos)

		#把分好的词和对应的修改后的词性分别存在两个文件里
		with open('./seg.txt', 'w+', encoding='utf-8') as sf,open('./text.txt', 'w+', encoding='utf-8') as tef, open('./pos.txt', 'w+', encoding='utf-8') as pf, open('./seg_spo.txt', 'w+',encoding='utf-8') as ssf:
			for i in range(self.total):
				# print(tr_spo[i][0]['predicate'])
				tef.write(self.tr_text[i])
				tef.write('\n')

				content = " ".join(segpos[i][0])
				sf.write(content)
				sf.write('\n')
				for j in range(len(self.tr_spo[i])):
					temp = content+" "+self.tr_spo[i][j]["subject"]+" "+self.tr_spo[i][j]["predicate"]+" "+self.tr_spo[i][j]["object"]
					ssf.write(temp)
					ssf.write('\n')


				content = " ".join(segpos[i][1])
				pf.write(content)
				pf.write('\n')



#处理label和schema
def label_schema():
	o_type = dict()
	s_type = dict()
	pre_type = dict()
	i,j,k = 0, 0, 0
	with open("../data/all_50_schemas", 'r+',encoding="UTF-8") as schemaf, open("./schema.txt", 'w+') as sf:
		pattern = "object_type\": \"(.*?)\", \"predicate\": \"(.*?)\", \"subject_type\": \"(.*?)\""
		for lines in schemaf:
			temp = re.findall(pattern, lines)#lines的类型是str
			if temp[0][0] not in o_type:
				o_type[temp[0][0]] = i
				i+=1
			if temp[0][2] not in s_type:
				s_type[temp[0][2]] = j
				j+=1
			pre_type[temp[0][1]] = k
			#print(temp[0][0])
			sf.write(temp[0][0]+':'+str(o_type[temp[0][0]])+' '+temp[0][1]+':'+str(k)+" "+temp[0][2]+":"+str(s_type[temp[0][2]])+'\n')
			k+=1
	schemaf.close()
	sf.close()
	return o_type, s_type, pre_type




if __name__ == "__main__":
	#o_type, s_type, pre_type = label_schema()
	#print('object:',o_type,'\n','subject:', s_type,'\n','predicate:', pre_type)
	dd = deal_data()
	dd.change_pos_build(mode = 0)#mode = 0时修改pos,为1时不修改

	#build_segpos(dd.tr_postag)
	dd.save_trainset()
	print("total:",dd.total)