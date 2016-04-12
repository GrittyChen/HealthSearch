#! /usr/bin/env python
#coding:utf-8

import os

def write_file(ret, query):
    #print os.getcwd()
    fp = open('./HealthSearch/src/webapp/static/data/label.txt', 'w')
    write_lines = [str(item[0]) + ' ' + item[1] + '\n' for item in ret]
    fp.write(query + '\n')
    fp.writelines(write_lines)
    fp.close()
