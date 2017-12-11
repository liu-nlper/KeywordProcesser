#!/usr/bin/env python
# -*- encoding: utf-8 -*-
__author__ = 'jxliu.nlper@gmail.com'


class KeywordExtractor(object):
    """
    中文keyword extractor

    Args:
        ignore: bool, default is false

    Attributes:
        keyword_trie_dict (dict): trie tree
        keyword_count (int): trie tree树中关键词数目
    """

    def __init__(self, ignore=False):
        self.keyword_trie_dict = dict()
        self.keyword_count = 0
        self._keyword_flag = '_type_'

        self._ignore = ignore

    def add_keyword(self, keyword, keyword_type=None):
        """
        Add keyword to keyword_trie_dict.

        Args:
            keyword (str): 关键词
            keyword_type (str): 关键词类型

        Examples:
            >>> keyword_extractor = KeywordExtractor()
            >>> keyword_extractor.add_keyword('苏州')
            >>> keyword_extractor.add_keyword('苏州', 'GPE')
        """
        if not keyword_type:
            keyword_type = keyword
        current_dict = self.keyword_trie_dict
        for char in keyword:
            current_dict = current_dict.setdefault(char, {})
        if self._keyword_flag not in current_dict:
            self.keyword_count += 1
            current_dict[self._keyword_flag] = keyword_type

    def add_keyword_from_list(self, keyword_list):
        """
        Add keywords from list.

        Args:
            keyword_list (list): list of keywords

        Examples:
            >>> keyword_extractor = KeywordExtractor()
            >>> keyword_extractor.add_keyword_from_list(['苏州', '江苏'])
        """
        for keyword in keyword_list:
            self.add_keyword(keyword)

    def add_keyword_from_dict(self, keyword_dict):
        """
        Add keywords from list.

        Args:
            keyword_dict (dict): keywords dict, {keyword: keyword_type}

        Examples:
            >>> keyword_extractor = KeywordExtractor()
            >>> keyword_extractor.add_keyword_from_dict({'苏州': 'GPE', '小明': 'PER'})
        """
        for keyword in keyword_dict:
            self.add_keyword(keyword, keyword_dict[keyword])

    def add_keyword_from_file(self, path, split='\t'):
        """
        Add keyword from file.

        Args:
            path (str): 关键词存放路径
            split (str): 分隔符，用于分隔关键词和关键词类型

        Examples:
            >>> keyword_extractor = KeywordExtractor()
            >>> path = 'path to your keywords'
            >>> keyword_extractor.add_keyword_from_file(path, split=',')
        """
        import codecs
        file_r = codecs.open(path, 'r', encoding='utf-8')
        line = file_r.readline()
        while line:
            line = line.strip()
            if not line:
                line = file_r.readline()
                continue
            items = line.split(split)
            if len(items) == 1:
                self.add_keyword(items[0])
            else:
                self.add_keyword(items[0], items[1])
            line = file_r.readline()
        file_r.close()

    def delete_keyword(self, keyword):
        """
        Delete keyword.

        Args:
            keyword (str): 关键词

        Return:
            state (bool): 删除是否成功

        Examples:
            >>> keyword_extractor = KeywordExtractor()
            >>> keyword_extractor.delete_keyword('your keyword')
        """
        current_dict = self.keyword_trie_dict
        level_node_list = []
        for char in keyword:
            if char not in current_dict:
                return False
            level_node_list.append((char, current_dict))
            current_dict = current_dict[char]

        if self._keyword_flag not in current_dict:
            return False

        level_node_list.append((self._keyword_flag, current_dict))
        for char, level_dict in level_node_list[::-1]:
            if len(level_dict) == 1:
                level_dict.pop(char)
            else:
                level_dict.pop(char)
                break
        self.keyword_count -= 1
        return True

    def delete_keyword_from_list(self, keyword_list):
        """
        Delete keywords from list
        Args:
            keyword_list (list): list of keyword
        """
        for keyword in keyword_list:
            self.delete_keyword(keyword)

    def _match_text(self, text, start, end):
        """
        Args:
            text (str): text
            start (int): 匹配的起始位置
            end (int): 匹配的结束位置

        Returns:
            end, entity_len, entity_type
        """
        current_dict = self.keyword_trie_dict
        index, entity_type = -1, ''

        for i in range(start, end):
            if text[i] == ' ' and self._ignore:
                continue
            if text[i] not in current_dict:
                if index == -1:
                    return start+1, 0, ''
                else:
                    return index+1, index+1-start, entity_type
            current_dict = current_dict[text[i]]
            if self._keyword_flag in current_dict:
                index = i
                entity_type = current_dict[self._keyword_flag]
        if index != -1:
            return index+1, index+1-start, entity_type
        return start+1, 0, ''

    def extract_keywords(self, text):
        """
        抽取text中存在的关键词

        Args:
            text (str): text

        Returns:
            keywords (list): list of  keywords and their positions

        Examples:
            >>> keyword_extractor = KeywordExtractor()
            >>> keyword_dict = {'苏州': 'GPE', '苏大': 'ORG', '苏州大学': 'ORG'}
            >>> keyword_extractor.add_keyword_from_dict(keyword_dict)
            >>> text = '我住在江苏省苏州市苏州大学333号,苏州大的小明'
            >>> keywords = keyword_extractor.extract_keywords(text)
            >>> # [[6, 8, 'GPE'], [9, 13, 'ORG'], [18, 20, 'GPE']]
        """
        keywords = []

        end, text_len = 0, len(text)
        while end < text_len:
            end, entity_len, entity_type = self._match_text(text, end, text_len)
            if entity_type:
                keywords.append([end-entity_len, end, entity_type])
        return keywords

    def extract_keywords_yield(self, text):
        """
        抽取text中存在的关键词

        Args:
            text (str): text
        """
        end, text_len = 0, len(text)
        while end < text_len:
            end, entity_len, entity_type = self._match_text(text, end, text_len)
            if entity_type:
                yield([end-entity_len, end, entity_type])

    def get_keyword_type(self, keyword):
        """
        获取keyword所对应的类型;若不存在，则返回None

        Args:
            keyword (str): keyword

        Returns:
            keyword_type (str): keyword type；若不存在，则返回None

        Examples:
            >>> keyword_extractor = KeywordExtractor()
            >>> keyword_dict = {'苏州': 'GPE', '北京': 'GPE'}
            >>> keyword_extractor.add_keyword_from_dict(keyword_dict)
            >>> keyword_extractor.get_keyword_type('北京')
            >>> # 'GPE'
        """
        current_dict = self.keyword_trie_dict
        for char in keyword:
            if char not in current_dict:
                return None
            current_dict = current_dict[char]
        if self._keyword_flag not in current_dict:
            return None
        return current_dict[self._keyword_flag]

    def contain_keyword(self, keyword):
        """
        判断keyword是否存在于trie tree中

        Args:
            keyword (str): keyword

        Returns:
            bool

        Examples:
            >>> keyword_extractor = KeywordExtractor()
            >>> keyword_dict = {'苏州': 'GPE', '北京': 'GPE'}
            >>> keyword_extractor.add_keyword_from_dict(keyword_dict)
            >>> keyword_extractor.contain_keyword('北京')
            >>> # True
            >>> keyword_extractor.contain_keyword('北京大学')
            >>> # False
        """
        current_dict = self.keyword_trie_dict
        for char in keyword:
            if char not in current_dict:
                return False
            current_dict = current_dict[char]
        if self._keyword_flag not in current_dict:
            return False
        return True

    def get_keywords(self, keyword_part='', current_dict=None):
        """
        获取所有的keywords

        Returns:
            keywords: list
        """
        keywords = dict()
        if current_dict is None:
            current_dict = self.keyword_trie_dict
        for char in current_dict:
            if char == self._keyword_flag:
                keywords[keyword_part] = current_dict[self._keyword_flag]
            else:
                keywords_ = self.get_keywords(keyword_part+char, current_dict[char])
                keywords.update(keywords_)
        return keywords


def demo():
    keyword_dict = {'苏州': 'GPE', '苏大': 'ORG', '北京': 'GPE', '苏州大学': 'ORG',
                    '苏有朋': 'PER', '苏有月': 'PER'}
    keyword_extractor = KeywordExtractor()
    keyword_extractor.add_keyword_from_dict(keyword_dict)
    print(keyword_extractor.keyword_count)
    text = '江苏省苏州市沧浪区干将东路333号苏州大学本部。'
    for item in keyword_extractor.extract_keywords_yield(text):
        print(item)

    # get_keywords
    print('all keywords:')
    print(keyword_extractor.get_keywords())


def demo2():
    keyword_dict = {'a-b': 'a-b'}
    keyword_extractor = KeywordExtractor(True)
    keyword_extractor.add_keyword_from_dict(keyword_dict)
    print(keyword_extractor.keyword_count)
    text = 'xxxa -  bxxx'
    for item in keyword_extractor.extract_keywords_yield(text):
        print(item)


if __name__ == '__main__':
    demo2()
