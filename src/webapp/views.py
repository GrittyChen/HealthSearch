#! /usr/bin/env python
#coding:utf-8

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from models import QuestionAnswer
from models import TagDict
from feature import Feature
from label import write_file
#from Translate.demo import *
import jieba
import math
import nltk
from __builtin__ import False

# Create your views here.
jieba.initialize()
QUERY = '' #store the query last time
RET_ANS = []#store the return answer last time
    
def Main_Page(request):
    return render(request, 'HSearch.html')

def ret_em(kw, a):
    sentence_list = nltk.sent_tokenize(a)
    res_sentence = ''
    no_select_sentence_list = []
    res_sentence_len = 0
    for sentence in sentence_list:
        is_select = False
        sentence_word = nltk.word_tokenize(sentence)
        sentence_temp = ''
        for word in sentence_word:
            if word.lower() in kw:
                sentence_temp += '<em>' +word + '</em> '
                is_select = True
            else:
                sentence_temp += word + ' '
        if is_select:
            res_sentence += sentence_temp
            res_sentence_len += len(sentence) + 1
        else:
            no_select_sentence_list.append(sentence)
    tmp = len(no_select_sentence_list)
    tp = 0
    while res_sentence_len < 210 and tp < tmp:
        res_sentence += no_select_sentence_list[tp] + ' '
        res_sentence_len += len(no_select_sentence_list[tp]) + 1
        tp += 1
    return res_sentence

def Is_rela(q, kw):
    q_list = nltk.word_tokenize(q)
    for k in kw:
        if k in q_list:
            return True
    return False

def showResults(request):
    global QUERY
    global RET_ANS
    query = request.GET['query']
    query = query.encode('UTF-8')
    if query == QUERY:
        return JsonResponse(RET_ANS, safe=False)
    else:
        QUERY = query
        #words = jieba.cut_for_search(query) #搜索分词
        ch_q = jieba.cut(query) #精准模式的分词
        kw_ch = [i for i in ch_q]
        tag_obj = TagDict.objects.filter(tag_ch__in = kw_ch) #
        cujiansuo = sum([tag.tag_class for tag in tag_obj], [])
        kw_en = [tag.tag_en for tag in tag_obj] #存储关键词;
        cujiansuo_res = sorted(set(cujiansuo), key=cujiansuo.index)
        qa_obj = QuestionAnswer.objects.filter(id__in=cujiansuo_res)
        print len(qa_obj)
        kw_en_len = len(kw_en)
        count_en = [0]*kw_en_len
        res_list = [] #最终返回的列表;
        kw = kw_en
        for item in qa_obj:
            q = item.question.lower()
            a = item.answer.lower()
            for i in range(kw_en_len):
                k = kw_en[i]
                if k in q or k in a:
                    count_en[i] += 1
            if Is_rela(q, kw_en):
                item_t = [item.id, item.question, ret_em(kw, item.answer), item.answer]
                res_list.append(item_t)
        D = len(res_list)
        Idf = []
        if not D == 0:
            Idf = [abs(math.log(D/float(t+1))) for t in count_en]
        theta1 = 1.0
        theta2 = 1.0
        theta3 = 1.0
        mmax = 0.0
        an_b = None
        for item in res_list:
            ans_sen = nltk.sent_tokenize(item[3])
            en_a = sum([nltk.word_tokenize(t) for t in ans_sen],[])
            en_q =  nltk.word_tokenize(item[1])
            socre_f = Feature(kw_ch, en_q, kw, en_a, Idf)
            sorce = theta1 * socre_f.length_feature() + sum(map(lambda(x):x*theta2, socre_f.word_feature())) + sum(map(lambda(x):x*theta3, socre_f.tfidf()))
            if mmax < sorce:
                mmax = sorce
                an_b = item
        RET_ANS = res_list
        write_file(res_list, query)
        return JsonResponse(RET_ANS, safe=False)

def showdetail(request):
    q_ch = request.GET['q']
    Id = int(request.GET['id'])
    res = QuestionAnswer.objects.get(id=Id)
    result_list = None
    if res:
        result_list = {'question':res.question, 'answer':res.answer}
    return render(request, 'detail.html', {'result_list':result_list, 'q_ch':q_ch})