# KeywordExtractor
使用python实现了一个简单的trie树结构，可增加/查找/删除关键词，用于中文的关键词匹配。

# 1 Installation
    $ git clone https://github.com/liu-nlper/KeywordExtractor.git
    $ cd KeywordExtractor
    $ python/python3 setup.py install

# 2 Usage
## 2.1 抽取关键词
- extract_keywords
- extract_keywords_yield

```python
from keyword_extract import KeywordExtractor

keyword_dict = {'苏州': 'GPE', '苏大': 'ORG', '沧浪区': 'GPE', '苏州大学': 'ORG'}
keyword_extractor = KeywordExtractor()
keyword_extractor.add_keyword_from_dict(keyword_dict)
print(keyword_extractor.keyword_count)  # 4

text = '江苏省苏州市沧浪区干将东路333号苏州大学本部。'

# extract_keywords
keywords = keyword_extractor.extract_keywords(text)
# [[3, 5, 'GPE'], [6, 9, 'GPE'], [17, 21, 'ORG']]

# extract_keywords_yield
for item in keyword_extractor.extract_keywords_yield(text):
    print(item)
```

## 2.2 添加关键词
- add_keyword: 添加单个关键词；
- add_keyword_from_list: 从列表中添加关键词；
- add_keyword_from_dict: 从字典中添加关键词，{关键词: 关键词类型}；
- add_keyword_from_file: 每个关键词占一行，若一行有多列，则第一列为关键词，第二列为关键词类型。

```python
keyword_extractor = KeywordExtractor()

# add_keyword
keyword_extractor.add_keyword('苏州')  # keyword_count is 1

# add_keyword_from_list
keyword_extractor.add_keyword_from_list(['江苏', '苏州'])  # keyword_count is 2

# add_keyword_from_dict
keyword_dict = {'苏州': 'GPE', '苏州大学': 'ORG'}
keyword_extractor.add_keyword_from_dict(keyword_dict)  # now, keyword_count is 3

# add_keyword_from_file
path = 'path_to_your_keywords'
keyword_extractor.add_keyword_from_file(path)
```

## 2.3 删除关键词
- delete_keyword
- delete_keyword_from_list

```python
keyword_extractor = KeywordExtractor()

# add_keyword
keyword_extractor.add_keyword('苏州', 'GPE')
keyword_extractor.add_keyword('北京', 'GPE')

# delete_keyword
keyword_extractor.delete_keyword('苏州')  # return True, keyword_count is 1
keyword_extractor.delete_keyword('苏州')  # return False

# delete_keyword_from_list
keyword_extractor.delete_keyword_from_list(['苏州', '江苏'])
```

## 2.4 获取关键词的类型
- get_keyword_type

```python
keyword_extractor = KeywordExtractor()

# add_keyword
keyword_extractor.add_keyword('苏州', 'GPE')
keyword_extractor.add_keyword('小明', 'PER')

# get_keyword_type
keyword_extractor.get_keyword_type('苏州')  # GPE
keyword_extractor.get_keyword_type('苏州大学')  # None
```

## 2.5 是否包含某个关键词
- contain_keyword

```python
keyword_extractor = KeywordExtractor()

# add_keyword
keyword_extractor.add_keyword('苏州', 'GPE')

# contain_keyword
keyword_extractor.contain_keyword('苏州')  # return True
keyword_extractor.delete_keyword('苏州')
keyword_extractor.contain_keyword('苏州')  # return False
```

## 2.6 获取所有关键词
- get_keywords

```python
keyword_extractor = KeywordExtractor()

# add_keyword
keyword_extractor.add_keyword('苏州', 'GPE')
keyword_extractor.add_keyword('苏州大学', 'ORG')

# get_keywords
keywords = keyword_extractor.get_keywords()
# ['苏州', '苏州大学']
```
