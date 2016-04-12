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
    fp = open('./webapp/static/data/test_data.txt', 'r')
    QAList = []
    TDList = []
    for line in fp:
        txt = line.strip()
        Q_index = txt.find('Q:')
        A_index = txt.find('A:')
        Tag_index = txt.find('TAGS:')
        question = txt[Q_index+2:A_index].strip()
        answer = txt[A_index+2:Tag_index].strip()
        tag_line = line[Tag_index+5:]
        tag_list = tag_line.strip().split(",")
        tag_list_fin = [t.strip().lower() for t in tag_list]
        QAList.append(QuestionAnswer(question = question, answer = answer, tags = tag_list_fin))
    fp.close()
    QuestionAnswer.objects.bulk_create(QAList)
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
    for i in range(tag_count):
        tag_ch = tag_ch_list_fin[i]
        tag_en = tag_en_list_fin[i]
        tag_class = []
        for j in op:
            if tag_en in j[1]:
                tag_class.append(int(j[0]))
        TDList.append(TagDict(tag_ch = tag_ch, tag_en = tag_en, tag_class = tag_class))
    TagDict.objects.bulk_create(TDList)
if __name__ == '__main__':
    main()
    print ('Data write successfully!')
