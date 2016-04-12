#! /usr/bin/env python
#coding=utf-8

import os
import nltk

class Feature:
    chinese_q = []
    english_q = []
    english_a = []
    keyword = []
    Idf = []
    def __init__(self, ch_q, en_q, kw, en_a, idf_l):
        self.chinese_q = ch_q
        self.english_q = en_q
        self.keyword = kw
        self.english_a = en_a
        self.Idf = idf_l

    def length_feature(self):
        len_en = len(self.english_q)
        len_ch = len(self.chinese_q)
        if len_en == len_ch:
            return 1.0
        else:
            temp = abs(len_en - len_ch)
            length = len_en + len_ch
            while temp < length:
                temp *= 10
            res = length/float(temp)
            return res #返回的是中文问题长度与英文问题长度的一个关系值,值越大代表相关性越低;

    def word_feature(self):
        res_q = 0.0
        res_a = 0.0
        txt_q = [i.lower() for i in self.english_q]
        txt_a = [i.lower() for i in self.english_a]
        for item in self.keyword:
            res_q += txt_q.count(item.lower())
            res_a += txt_a.count(item.lower())
        return [res_q, res_a] #返回结果是所有关键词在问题和答案中分别出现的次数;

    def tfidf(self):
        tfidf_res = []
        text = sum([self.english_q, self.english_a],[])
        text = [item.lower() for item in text]
        L = float(len(text))
        for i in range(len(self.keyword)):
            word = self.keyword[i]
            tf = 0.0
            for item in text:
                if word.lower() == item:
                    tf += 1.0
            tf = tf/L
            tfidf_res.append(tf*self.Idf[i])
        return tfidf_res #返回值是所有keyword的tfidf值
