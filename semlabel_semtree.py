#coding=utf-8
from pyltp import SementicRoleLabeller
from pyltp import Parser
import final_process
import numpy as np
import gc

ltp_path = "ltp-models/3.4.0/ltp_data_v3.4.0/"
TR_SIZE = 99996#99996	#
BATCH = 1000
TOT_BATCH = int(TR_SIZE/BATCH)+1
noun = {'n', 'ns','nh','ws','nz','nl','ni'}

spo_count = []

parser = Parser()
parser.load(ltp_path + "parser.model")
labeller = SementicRoleLabeller()
labeller.load(ltp_path + "pisrl.model")#"pisrl_win.model")

class Parser_SementicRole:
	def __init__(self, segwords, wordspos):
		self.seg_words = segwords	#分好的词
		self.words_pos = wordspos	#wordspos是分好的词对应的词性（已经按照ltp格式修改过了）
		self.total = len(segwords) 	#句子数
		self.all_arcs = self.parse()
		self.all_roles = self.SementicRoleLabeller()


	def parse(self):
		# 从1开始
		all_arcs = []

		for i in range(self.total):
			arcs = parser.parse(self.seg_words[i], self.words_pos[i])

			all_arcs.append(arcs)

		return all_arcs

	def SementicRoleLabeller(self):
		#从0开始
		all_roles = []

		for i in range(self.total):
			roles = labeller.label(self.seg_words[i], self.words_pos[i], self.all_arcs[i])

			all_roles.append(roles)

		return all_roles

#为句子中的每个词语维护一个保存句法依存儿子节点的字典
def build_childdict(arcs):
	child_dict_list = [dict() for _ in range(len(arcs)+1)]
	i = 0
	temp_dict = dict()
	for item in arcs:
		child_dict_list[item.head][item.relation] = i
		i+=1

	return child_dict_list


def extract_by_arc(arcs,seg_words,words_pos):#arcs是一个句子的依存句法分析
	svos = []
	child_dict = build_childdict(arcs)
	#print("child_dict:",child_dict)


	for index in range(len(arcs)):
		if child_dict[index+1]:
			if (words_pos[index] == 'v' and seg_words[index] != '是' and seg_words[index] != '于') or arcs[index].relation == 'HED':
				# 主谓宾提取
				if 'SBV' in child_dict[index+1] and 'VOB' in child_dict[index+1]:
					e1 = child_dict[index+1]['SBV']
					e2 = child_dict[index+1]['VOB']
					r = index
					svos.append([seg_words[e1], seg_words[r], seg_words[e2]])
					if 'COO' in child_dict[e2]:#如果宾语有COO的话，再生成一组三元组
						e2 = child_dict[e2]['COO']
						svos.append([seg_words[e1], seg_words[r], seg_words[e2]])  # 找到一个三元组
					#e2还原
					e2 = child_dict[index+1]['VOB']
					if 'COO' in child_dict[index+1]:#如果动词有COO的话
						r = child_dict[index+1]['COO']
						svos.append([seg_words[e1], seg_words[r], seg_words[e2]])  # 找到一个三元组
						if 'COO' in child_dict[e2]:#如果宾语有COO的话，再生成一组三元组
							e2 = child_dict[e2]['COO']
							svos.append([seg_words[e1], seg_words[r], seg_words[e2]])  # 找到一个三元组

				# 定语后置，动宾关系
				if arcs[index].relation == 'ATT':
					if 'VOB' in  child_dict[index+1]:
						e1 = arcs[index].head-1
						r = index
						e2 = child_dict[index+1]['VOB']
						svos.append([seg_words[e1], seg_words[r], seg_words[e2]])  # 找到一个三元组

				# 含有介宾关系的主谓动补关系
				if 'SBV' in child_dict[index + 1] and 'CMP' in child_dict[index + 1]:
					e1 = child_dict[index+1]['SBV']
					cmp_index = child_dict[index+1]['CMP']
					r_word = seg_words[index] + seg_words[cmp_index]
					if 'POB' in child_dict[cmp_index + 1]:
						e2 = child_dict[cmp_index + 1]['POB']
						svos.append([seg_words[e1], r_word, seg_words[e2]])  # 找到一个三元组

	return svos

#找出index（start, end）中最好的名词
def pick_noun(arg,seg_words,words_pos):
	start = arg.range.start
	end = arg.range.end
	ans_word = ''
	flag = 0
	for i in range(start,end+1):
		if words_pos[i] in noun:
			if flag == 1 or ans_word == '':		#如果有多个不相连的名词类，取第一个
				ans_word = ans_word + seg_words[i]
			flag = 1
		else:
			flag = 0
	if ans_word == '':
		ans_word = seg_words[start]

	return ans_word


def tri_out(arcs, roles,seg_words,words_pos):
	'''
	arcs是第i个的依存分析
	roles是第i个的语义角色抽取
	arc是第i个句子的第j项，role是第i个句子的第k项
	arc.head是依存分析的父结点（从1开始），arc.relation是依存分析的关系
	role.index是语义角色的句子中编号（从0开始），role.arguments[t]是附属的参数关系：.name是名称.range.start, .range.end表示该单位的开始和截止位置
	'''
	tri = []
	if len(seg_words) <3:
		tri = [['夏芢国','出生于','天津']]
	else:
		j = 0
		#Ai_exist = -1
		find_a = dict()#{index:[arg,arg...],index:[arg,arg...]...}
		find_a1 = dict()

		for role in roles:
			#判断是否存在主语和核心谓词,找出所有
			find_a[role.index] = []
			find_a1[role.index] = []
			for arg in role.arguments:
				if arg.name == 'A0' or arg.name == 'A2' or arg.name == 'A3' or arg.name == 'A4' or arg.name == 'A5':
					find_a[role.index].append(arg)	#保存一整个项
				if arg.name == 'A1':
					find_a1[role.index].append(arg)

			j += 1
		#print("find_a:",find_a)
		#print("find_a1:", find_a1)

		if roles:
			for key,value in find_a.items():#key是role.index
				i_a = 0
				i_a1 = 0
				while i_a < len(value):
					a = pick_noun(value[i_a], seg_words, words_pos)
					#print("need pick a")
					# 如果对于一个role.index来说，A0(2,3,4,5)和A1都存在时
					while i_a1 < len(find_a1[key]):
						a1 = pick_noun(find_a1[key][i_a1], seg_words, words_pos)
						#print("need pick a1")
						if a != '' and a1 != '':
							tri.append([a, seg_words[key], a1])  # 取A0(2,3,4,5)和role.index和A1作为一个三元组
						i_a1 += 1
					# 存在A0(2,3,4,5)，补充A1也存在的情况，并且A1不存在的情况也要找出三元组
					start = key
					end = key
					while 1:
						if arcs[start].relation == 'VOB':
							end = arcs[start].head-1
							if words_pos[end] in noun:
								tri.append([a, seg_words[start], seg_words[end]])	#找到一个三元组
							break
						elif arcs[start].relation == 'COO':
							start = arcs[start].head-1
						else:
							break

					i_a += 1
		#print(seg_words)
		#print("tri:", tri)
		if len(tri) == 0:
			svos = extract_by_arc(arcs,seg_words,words_pos)
			tri = svos
		#print("tri+svo:", tri)

		if len(tri) == 0:
			r = 0
			i = 0
			flag = 0
			for i in range(len(seg_words)):
				if flag == 0 and words_pos[i] == 'v':#predicate
					r = i
					flag = 1
				elif flag == 1 and words_pos[i] in noun:#object
					break
			for j in range(r):#subject
				if words_pos[r-j-1] in noun:
					break
			if j == 0 and words_pos[0] not in noun:
				flag = 0
			if flag == 1:
				tri.append([seg_words[r-j-1], seg_words[r], seg_words[i]])

		if len(tri) == 0:
			tri.append([seg_words[0], seg_words[int(len(seg_words)/2)], seg_words[len(seg_words)-1]])


	return tri



if __name__ == "__main__":
	segwords = []
	wordspos = []

	D = final_process.deal_data()
	tr_postag = D.tr_postag
	for item in tr_postag:
		s_temp = []
		for index in range(len(item)):  # item[index]指的是{'pos': 'r', 'word': '如何'}
			s_temp.append(item[index]['word'])
		segwords.append(s_temp)

	with open('./final/test_pos.txt', 'r', encoding= 'utf-8') as pf:
		# for s_line in sf.readlines():
		# 	s_line = s_line.strip()
		# 	s_temp = s_line.split(' ')
		# 	segwords.append(s_temp)#segwords是分好的词
		for p_line in pf.readlines():
			p_line = p_line.strip()
			p_temp = p_line.split(' ')
			wordspos.append(p_temp)#wordspos是分好的词对应的词性（已经按照ltp格式修改过了）
	pf.close()

	segwords = np.array(segwords)
	wordspos = np.array(wordspos)

	# segwords = segwords[90000:]
	# wordspos = wordspos[90000:]

	segspo_file = './finalymtan/test_segspo_ymtan.txt'
	spo_count_file = './finalymtan/spo_count_ymtan.txt'

	#segwords = segwords[]

	print("读入分词和词性标注 done!")
	start = 0
	ttt = 0
	for tt in range(TOT_BATCH):
		print("-------------第",tt,"个batch-------------")

		start = tt*BATCH
		if (start+BATCH)>TR_SIZE:
			break
		tmp_segwords = segwords[start:start+BATCH]
		tmp_wordspos = wordspos[start:start+BATCH]
		#print(len(tmp_segwords), len(tmp_wordspos),'\n')
		ps = Parser_SementicRole(tmp_segwords, tmp_wordspos)

		with open(segspo_file, 'a',encoding='utf-8') as tssf,open(spo_count_file,'a',encoding='utf-8') as scf:
			for i in range(len(tmp_segwords)):

				content = " ".join(tmp_segwords[i])
				#print("content:", content)

				#print(len(ps.seg_words[i]), len(ps.words_pos[i]))
				if(len(ps.seg_words[i])!=len(ps.words_pos[i])):
					off = len(ps.seg_words[i])-len(ps.words_pos[i])
					for i in range(off):
						ps.seg_words[i].pop()
				tri = tri_out(ps.all_arcs[i], ps.all_roles[i], ps.seg_words[i], ps.words_pos[i])

				if i%200 == 0:
					print("-------------第", ttt, "句话-------------")
					print('tri:',tri)
				tri_length = len(tri)
				spo_count.append(tri_length)
				scf.write(str(tri_length))
				scf.write(' ')
				for j in range(tri_length):
					ctemp = content + " " + tri[j][0] + " " + tri[j][1] + " " + tri[j][2]
					tssf.write(ctemp)
					tssf.write('\n')
				ttt+=1
			#print("len(segwords):", len(tmp_segwords))

	tmp_segwords = segwords[start:]
	tmp_wordspos = wordspos[start:]
	ps = Parser_SementicRole(tmp_segwords, tmp_wordspos)

	with open(segspo_file,'a',encoding='utf-8') as tssf,open(spo_count_file,'a',encoding='utf-8') as scf:
		for i in range(len(tmp_segwords)):
			content = " ".join(tmp_segwords[i])
			#print("content:",content)
			tri = tri_out(ps.all_arcs[i], ps.all_roles[i],ps.seg_words[i],ps.words_pos[i])
			print('tri:', tri)
			tri_length = len(tri)
			spo_count.append(tri_length)
			scf.write(str(tri_length))
			scf.write(' ')
			for j in range(tri_length):
				ctemp = content+" "+tri[j][0]+" "+tri[j][1]+" "+tri[j][2]
				tssf.write(ctemp)
				tssf.write('\n')


	# with open('./final/spo_count1.txt','a',encoding='utf-8') as scf1:
	# 	for item in spo_count:
	# 		scf1.write(str(item))
	# 		scf1.write(' ')
	print("spo_count:", spo_count)
	print("len spo_count:",len(spo_count))
	parser.release()
	labeller.release()

