# use-LTP
Information Extraction of SKE dataset (http://lic2019.ccf.org.cn/)

##1. 竞赛任务
给定schema约束集合及句子sent，其中schema定义了关系P以及其对应的主体S和客体O的类别，例如（S_TYPE:人物，P:妻子，O_TYPE:人物）、（S_TYPE:公司，P:创始人，O_TYPE:人物）等。 任务要求参评系统自动地对句子进行分析，输出句子中所有满足schema约束的SPO三元组知识Triples=[(S1, P1, O1), (S2, P2, O2)…]。
输入/输出:
(1) 输入:schema约束集合及句子sent
(2) 输出:句子sent中包含的符合给定schema约束的三元组知识Triples
##2. 数据简介
使用的SKE数据集是业界规模最大的基于schema的中文信息抽取数据集，其包含超过43万三元组数据、21万中文句子及50个已定义好的schema，表1中展示了SKE数据集中包含的50个schema及对应的例子。数据集中的句子来自百度百科和百度信息流文本。数据集划分为17万训练集，2万验证集和2万测试集。
序号   主体S的类别  关系  客体O的类别   举例
1	地点	海拔	Number	{"object_type": "Number", "predicate": "海拔", "object": "2,240米", "subject_type": "地点", "subject": "卡萨布兰卡火山"}
2	电视综艺	嘉宾	人物	{"object_type": "人物", "predicate": "嘉宾", "object": "黄小琥", "subject_type": "电视综艺", "subject": "全能星战"}
3	电视综艺	主持人	人物	{"object_type": "人物", "predicate": "主持人", "object": "撒贝宁", "subject_type": "电视综艺", "subject": "梦想星搭档"}
4	歌曲	歌手	人物	{"object_type": "人物", "predicate": "歌手", "object": "李克勤", "subject_type": "歌曲", "subject": "爱不释手"}
5	歌曲	所属专辑	音乐专辑	{"object_type": "音乐专辑", "predicate": "所属专辑", "object": "爱不释手 新城唱好音乐大派对", "subject_type": "歌曲", "subject": "爱不释手"}
6	歌曲	作词	人物	{"object_type": "人物", "predicate": "作词", "object": "林夕", "subject_type": "歌曲", "subject": "爱不释手"}
7	歌曲	作曲	人物	{"object_type": "人物", "predicate": "作曲", "object": "陈辉阳", "subject_type": "歌曲", "subject": "爱不释手"}
8	国家	官方语言	语言	{"object_type": "语言", "predicate": "官方语言", "object": "意大利语", "subject_type": "国家", "subject": "意大利"}
9	国家	首都	城市	{"object_type": "城市", "predicate": "首都", "object": "羊苴咩城", "subject_type": "国家", "subject": "大理国"}
10	行政区	面积	Number	{"object_type": "Number", "predicate": "面积", "object": "188平方公里", "subject_type": "行政区", "subject": "河西镇"}
