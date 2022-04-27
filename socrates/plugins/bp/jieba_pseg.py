# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 21:14:26 2021

@author: Roc
"""

import jieba
import jieba.posseg as pseg

def open_txt(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.readlines()


path = 'Zhihu_test.txt'
MAX_LENGTH = 50
lst = open_txt(path)

for Q, A in [line.strip('\n').split('\t') for line in lst]:
    words = pseg.cut(Q)
    nouns = [w.word for w in words if 'n' in w.flag.lower()]
    A_lst = jieba.cut_for_search(A)
    

