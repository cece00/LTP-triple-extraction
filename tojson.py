
import json

def spo_c():
	spo_count =[]
	with open("../spo_count.txt", 'r', encoding='utf-8') as scf:
		for line in scf.readlines():
			line = line.strip()
			line = line.split(' ')
			spo_count =spo_count + list(map(int, line))
	scf.close()

	return spo_count



def data2json():
	res = []
	res_dict = dict()
	spo_count = spo_c()
	all_spo = []
	all_text = []
	with open("../5_spo_lstm.txt",'r',encoding='utf-8') as spof:
		# subject,object,o_type,predicate,s_type
		for line in spof.readlines():
			line = line.strip('\n')
			all_spo.append(line.split(' '))
	with open("./test_text.txt",'r',encoding='utf-8') as ttf:
		for line in ttf.readlines():
			line = line.strip()
			all_text.append(line)
	t = 0
	#print(all_text)
	with open('../result_lstm.json', 'w', encoding='utf-8') as json_file:
		for i in range(len(spo_count)):
			res_dict["text"] = all_text[i]
			spo_list = []
			for j in range(spo_count[i]):
				spo_temp = dict()
				spo_temp["object_type"] = all_spo[t][2]
				spo_temp["predicate"] = all_spo[t][3]
				spo_temp["object"] = all_spo[t][1]
				spo_temp["subject_type"] = all_spo[t][4]
				spo_temp["subject"] = all_spo[t][0]
				spo_list.append(spo_temp)
				t+=1
			#print(i,t,"spo_list:",spo_list)
			res_dict["spo_list"] = spo_list

			json_str = json.dumps(res_dict,ensure_ascii=False)#, indent=4
			json_file.write(json_str)
			json_file.write('\n')
		print(len(spo_count))



if __name__ == '__main__':
	data2json()
