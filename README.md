# KeywordProcesser
使用python实现了一个简单的trie树结构，可增加/查找/删除关键词，用于中文的关键词匹配、停用词删除等。

# 1 Installation
    $ git clone https://github.com/liu-nlper/KeywordProcesser.git
    $ cd KeywordProcesser
    $ python/python3 setup.py install

# 2 Usage

## 2.1 抽取关键词

- extract_keywords
- extract_keywords_yield
- extract_keywords_from_list
- extract_keywords_from_list_yield

```python
from keyword_extract import KeywordProcesser

keyword_dict = {'苏州': 'GPE', '苏大': 'ORG', '沧浪区': 'GPE', '苏州大学': 'ORG'}
keyword_processer = KeywordProcesser(keyword_dict)
print(keyword_processer.keyword_count)  # 4

text = '江苏省苏州市沧浪区干将东路333号苏州大学本部。'

# extract_keywords
keywords = keyword_processer.extract_keywords(text)
# [[3, 5, 'GPE'], [6, 9, 'GPE'], [17, 21, 'ORG']]

# extract_keywords_yield
for item in keyword_processer.extract_keywords_yield(text):
    print(item)

# 匹配时忽略空格
text = '苏州 大学'
keywords = keyword_processer.extract_keywords(text)
# [[0, 2, 'GPE']] -> '苏州'
keyword_processer.set_ignore_space(True)
keywords = keyword_processer.extract_keywords(text)
# [[0, 5, 'ORG']] -> '苏州 大学'

# 从词序列中匹配关键词
keyword_dict = {'江苏省': 'GPE', '苏大': 'ORG', '北京': 'GPE', '苏州大学': 'ORG',
                '苏有朋': 'PER', '苏有月': 'PER'}
keyword_processer = KeywordProcesser(keyword_dict)
words = ['江苏省', '苏州市', '沧浪区', '干将东路', '333号', '苏州大学', '本部', '。']
keywords = keyword_processer.extract_keywords_from_list(words)
print(keywords)
# [['江苏省', 0], ['苏州大学', 5]]
```

## 2.2 从文本中删除关键词

- remove_keywords_in_text: 从文本中删除关键词
- remove_keywords_in_words: 从词序列中删除关键词

```python
stopwords = ['、', '，', '。', '的', '对', '和', '这个', '一切']
sentence = '这个时间落伍的计时机无意中对人生包涵的讽刺和感伤，深于一切语言、一切啼笑。'
keyword_processer = KeywordProcesser(stopwords)
sentence = keyword_processer.remove_keywords_in_text(sentence)
# 时间落伍计时机无意中人生包涵讽刺感伤深于语言啼笑

keyword_processer = KeywordProcesser(stopwords)
words = ['这个', '时间', '落伍', '的', '计时机', '无意', '中', '对', '人生', '包涵',
         '的', '讽刺', '和', '感伤', '，', '深于', '一切', '语言', '、', '一切', '啼笑', '。']
print(words)
words = keyword_processer.remove_keywords_in_words(words)
print(''.join(words))
# 时间落伍计时机无意中人生包涵讽刺感伤深于语言啼笑
```

## 2.3 添加关键词
- add_keyword: 添加单个关键词；
- add_keyword_from_list: 从列表中添加关键词；
- add_keyword_from_dict: 从字典中添加关键词，{关键词: 关键词类型}；
- add_keyword_from_file: 每个关键词占一行，若一行有多列，则第一列为关键词，第二列为关键词类型。

```python
keyword_processer = KeywordProcesser()

# add_keyword
keyword_processer.add_keyword('苏州')  # keyword_count is 1

# add_keyword_from_list
keyword_processer.add_keyword_from_list(['江苏', '苏州'])  # keyword_count is 2

# add_keyword_from_dict
keyword_dict = {'苏州': 'GPE', '苏州大学': 'ORG'}
keyword_processer.add_keyword_from_dict(keyword_dict)  # now, keyword_count is 3

# add_keyword_from_file
path = 'path_to_your_keywords'
keyword_processer.add_keyword_from_file(path, split='\t')
```

## 2.4 删除关键词
- delete_keyword
- delete_keyword_from_list

```python
keyword_processer = KeywordProcesser()

# add_keyword
keyword_processer.add_keyword('苏州', 'GPE')
keyword_processer.add_keyword('北京', 'GPE')

# delete_keyword
keyword_processer.delete_keyword('苏州')  # return True, keyword_count is 1
keyword_processer.delete_keyword('苏州')  # return False

# delete_keyword_from_list
keyword_processer.delete_keyword_from_list(['苏州', '江苏'])
```

## 2.5 获取关键词的类型
- get_keyword_type

```python
keyword_processer = KeywordProcesser()

# add_keyword
keyword_processer.add_keyword('苏州', 'GPE')
keyword_processer.add_keyword('小明', 'PER')

# get_keyword_type
keyword_processer.get_keyword_type('苏州')  # GPE
keyword_processer.get_keyword_type('苏州大学')  # None
```

## 2.6 是否包含某个关键词
- contain_keyword

```python
keyword_processer = KeywordProcesser()

# add_keyword
keyword_processer.add_keyword('苏州', 'GPE')

# contain_keyword
keyword_processer.contain_keyword('苏州')  # return True
keyword_processer.delete_keyword('苏州')
keyword_processer.contain_keyword('苏州')  # return False
```

## 2.7 获取所有关键词
- get_keywords

```python
keyword_processer = KeywordProcesser()

# add_keyword
keyword_processer.add_keyword('苏州', 'GPE')
keyword_processer.add_keyword('苏州大学', 'ORG')

# get_keywords
keywords = keyword_processer.get_keywords()
# {'苏州': 'GPE', '苏州大学': 'ORG'}
```

# Updating

 - 2018-06-21:
    * 添加删除关键词功能，可用于停用词的删除；
    * 输入可以是词序列(list)或者纯文本(str)。

## TODO

- [] 关键词替换
- [] other...
