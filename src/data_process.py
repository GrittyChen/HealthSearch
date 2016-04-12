#! /usr/bin/env python
#coding:utf-8

def main():
    fp = open('./webapp/static/data/data_fin.txt', 'r')
    datalines = fp.readlines()
    fp.close()
    length = len(datalines) / 3
    QAT_List1 = [datalines[3*k]+datalines[3*k+1] for k in range(length)]
    len1 = len(QAT_List1)
    QAT_List2 = sorted(set(QAT_List1), key=QAT_List1.index)
    len2 = len(QAT_List2)
    print len1
    print len2

if __name__ == '__main__':
    main()
