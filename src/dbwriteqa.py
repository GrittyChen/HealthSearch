#! /usr/bin/env python
#coding:utf-8

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HealthSearch.settings')
import django

if django.VERSION >= (1, 7):
    django.setup()

def main():
    from webapp.models import QuestionAnswer
    from webapp.models import TagDict
    QuestionAnswer.objects.all().delete()#清空表
    TagDict.objects.all().delete()#清空表
    fp = open('./webapp/static/data/data_fin2.txt', 'r')
    datalines = fp.readlines()
    fp.close()
    length = len(datalines) / 3
    QAList = [QuestionAnswer(question = datalines[3*k].strip(), answer = datalines[3*k+1], tags = [t.strip().lower() for t in datalines[3*k+2].split(',')]) for k in range(length)]
    QuestionAnswer.objects.bulk_create(QAList)
    print 'QAList write successful'
    obj = QuestionAnswer.objects.all()
    op = [[item.id,item.tags] for item in obj]
    fp1 = open('./webapp/static/data/tag_test.txt', 'r')
    fp2 = open('./webapp/static/data/tag_test_ch.txt', 'r')
    tag_en_list = fp1.readlines()
    tag_ch_list = fp2.readlines()
    fp1.close()
    fp2.close()
    tag_en_list_fin = [t.strip() for t in tag_en_list]
    tag_ch_list_fin = [t.strip() for t in tag_ch_list]
    tag_count = len(tag_en_list_fin)
    TDList = [TagDict(tag_ch = tag_ch_list_fin[i], tag_en = tag_en_list_fin[i], tag_class = [int(j[0]) for j in op if tag_en_list_fin[i] in j[1]]) for i in range(tag_count)]
    TagDict.objects.bulk_create(TDList)
    print 'TDlist write successful'
if __name__ == '__main__':
    main()
    print ('Data write successfully!')
