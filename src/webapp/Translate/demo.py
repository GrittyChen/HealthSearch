#/usr/bin/env python
#coding=utf8
 
import httplib
import md5
import urllib
import random
import json

def translate(q, fromLang, toLang):
    appid = '20160309000015094'
    secretKey = 'gxPA4JVmvYVE9JbJZfsu' 
    httpClient = None
    myurl = '/api/trans/vip/translate'
    salt = random.randint(1, 100000)
    sign = appid+q+str(salt)+secretKey
    m1 = md5.new()
    m1.update(sign)
    sign = m1.hexdigest()
    myurl = myurl+'?appid='+appid+'&q='+urllib.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign     
    try:
        httpClient = httplib.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        #response是HTTPResponse对象
        response = httpClient.getresponse()
        ret = None
        #trans_res =  response.read()
        trans_res = json.load(response)
        if trans_res['trans_result']:
           return trans_res['trans_result'][0]['dst']
        else:
           return None 
    except Exception, e:
        print e
        return None
    finally:
        if httpClient:
            httpClient.close()
