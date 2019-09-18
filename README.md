# use-LTP
Information Extraction of SKE dataset (http://lic2019.ccf.org.cn/)

## 1. 竞赛任务
给定schema约束集合及句子sent，其中schema定义了关系P以及其对应的主体S和客体O的类别，例如（S_TYPE:人物，P:妻子，O_TYPE:人物）、（S_TYPE:公司，P:创始人，O_TYPE:人物）等。 任务要求参评系统自动地对句子进行分析，输出句子中所有满足schema约束的SPO三元组知识Triples=[(S1, P1, O1), (S2, P2, O2)…]。
输入/输出:
(1) 输入:schema约束集合及句子sent
(2) 输出:句子sent中包含的符合给定schema约束的三元组知识Triples
## 2. 数据简介
使用的SKE数据集是业界规模最大的基于schema的中文信息抽取数据集，其包含超过43万三元组数据、21万中文句子及50个已定义好的schema，表1中展示了SKE数据集中包含的50个schema及对应的例子。数据集中的句子来自百度百科和百度信息流文本。数据集划分为17万训练集，2万验证集和2万测试集。

| 序号        | 主体S的类别           | 关系  | 客体O的类别   | 举例   |
|: ----- :|:---------:|:---------:|:---------:|:---------------------------------:|
| 1 |地点 |海拔 | Number |{"object_type": "Number", "predicate": "海拔", "object": "2,240米", "subject_type": "地点", "subject": "卡萨布兰卡火山"}|
| 2 |电视综艺 |嘉宾 | 人物 |{"object_type": "人物", "predicate": "嘉宾", "object": "黄小琥", "subject_type": "电视综艺", "subject": "全能星战"}|

