# IR use LTP
Information Extraction of SKE dataset (http://lic2019.ccf.org.cn/)

### 1. 竞赛任务
给定schema约束集合及句子sent，其中schema定义了关系P以及其对应的主体S和客体O的类别，例如（S_TYPE:人物，P:妻子，O_TYPE:人物）、（S_TYPE:公司，P:创始人，O_TYPE:人物）等。 任务要求参评系统自动地对句子进行分析，输出句子中所有满足schema约束的SPO三元组知识Triples=[(S1, P1, O1), (S2, P2, O2)…]。
输入/输出:
(1) 输入:schema约束集合及句子sent
(2) 输出:句子sent中包含的符合给定schema约束的三元组知识Triples
### 2. 数据简介
使用的SKE数据集是业界规模最大的基于schema的中文信息抽取数据集，其包含超过43万三元组数据、21万中文句子及50个已定义好的schema，表1中展示了SKE数据集中包含的50个schema及对应的例子。数据集中的句子来自百度百科和百度信息流文本。数据集划分为17万训练集，2万验证集和2万测试集。

| 序号     | 主体S的类别      | 关系  | 客体O的类别   | 举例   |
|---|------|-----|-----|----------------|
| 1 |地点 |海拔 | Number |{"object_type": "Number", "predicate": "海拔", "object": "2,240米", "subject_type": "地点", "subject": "卡萨布兰卡火山"}|
| 2 |电视综艺 |嘉宾 | 人物 |{"object_type": "人物", "predicate": "嘉宾", "object": "黄小琥", "subject_type": "电视综艺", "subject": "全能星战"}|
   
对于三元组抽取任务，我们认为可能分为主体客体抽取、关系抽取两个部分。后者会利用前者的信息完善结果，所以我们需要先实现主体客体模型，再实现关系模型。这样拆解保证了问题的可行性，也保证了团队合作的高效和均衡。

### 3.our model
##### 1)系统架构
我们将问题拆解为两部分，所以针对这两部分独立设计结构。
(1)	三元组模型：通过依存句法+语义角色标注的方法，提取依据predicate的主体客体。
(2)	关系模型：Keras框架+CNN/Bi-LSTM，预测句子对应的predicate。
(3)	系统架构 = 关系模型 + 三元组模型。

##### 2)关系模型介绍
**处理数据**  
我们首先从训练样本train_data.json中抽取出10000条样本作为训练语料，并依据正则表达式划分text（文本）、predicate（关系）、object_type（客体类型）、object（客体）、subject（主体）、subject_type（主体类型）。之后我们给50个关系赋值0-49，并为每条样本打上标签。

**搭建模型**  
经过调研，我们发现CNN和Bi-LSTM在处理文本时，具有相对较好的性能。CNN构造神经网络，通过误差回馈修正权重；Bi-LSTM双向考虑上下文，充分利用已知信息。这两这都适用于我们这个任务，所以我们采用了Keras框架+CNN和Keras+Bi-LSTM进行模型的搭建。

**环境**  
--Python 3 + Keras(基于tensorflow)  
--LTP3.4.0

**code**  
written by 	qsy  
1. pre_process.py（无输出）  
注意设置TR_SIZE的大小，该变量为训练集的大小（即训练集的句子数）  
2. the_model.py  
会调用deal_data.py，get_label.py，pre_model.py三个文件，其中若有TR_SIZE，请注意设置  
3. final_process.py  
修改pre_process.py训练集路径为测试集路径，生成测试文件  
4. semlabel_semtree.py  
生成三元组并和句子一起保存为测试文件final_data.txt，每一行为以空格隔开的词的句子加上三元组，并注意保存每个句子三元组的数量  
5. predict.py  
使用final_data.txt预测类别，转换为五元组，写入final_label.py文件  
6. tojson.py  
使用final_label.py写入json文件：  
需要 1）原始句子 2）五元组list  
格式：  
```python
{  
    "text": "input sentence", // must be exactly the same as the given original sentence  
         "spo_list":[{    //all spo triples extracted from text  
                "object_type":"XX",    // object type  
                "predicate":"XX",      // predicate mentioned in text  
                "object":"o_value",   // object value  
                "subject_type":"XX",   // subject type  
                "subject":"s_value".   // subject value  
               },   
    ……  
             ]  
    }  
```



**参考paper：**  
http://www.doc88.com/p-1436368975920.html  
https://www.cnblogs.com/herosoft/p/8134213.html
