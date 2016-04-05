import urllib
import pandas as pd
import bs4
import requests
from bs4 import BeautifulSoup
import queue
import threading
import traceback
import time
import re
import json
from time import ctime,sleep
import redis
import database_list

class ConsumerQQ(threading.Thread):
    def __init__(self,database):
        super().__init__()
        threading.Thread.__init__(self)
        self.q = database

    def run(self):
        print ('QQ:starting...')
        while True:
            # print (self.f.flag_QQ)

            # print (self.data.qsize())
            if self.q.flag_QQ is False or len(self.q.data.keys()) != 0:
                for key_word in self.q.data.keys():
                    Flag = False
                    value = self.q.data.get(key_word)
                    # print(key_word)

                    try:
                        # print('腾讯')
                        # key_word = self.q.data.get()
                        # print(key_word)
                        # key_word = '微信'

                        url = 'http://sj.qq.com/myapp/searchAjax.htm?kw=' +key_word
                        headers = {
                            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
                        response = requests.get(url, headers=headers).text
                        # print (response)
                        # req = urllib.Request(url, headers)
                        # content = urllib.urlopen(url, timeout=25).read()
                        # print (content)
                        content_re = re.compile('flag(.*?)versionCode')
                        content = content_re.findall(response)
                        # print(content)


                    except:
                        self.q.queueQQ.set(key_word,value)
                        self.q.data.delete(key_word)
                        # print (key_word)
                        continue;

                    for i in range(0, len(content)):
                        # print(i)
                        childcontent = content[i]
                        appName_re = re.compile('\"appName\":\"([\\s\\S]*?)\"')
                        pkgName_re = re.compile('\"pkgName\":\"([\\s\\S]*?)\"')
                        appName = appName_re.findall(childcontent)[0]
                        pkgName = pkgName_re.findall(childcontent)[0]
                        appName = appName.lower()
                        # print (appName)
                        # print (key_word)
                        if appName == key_word:
                            # print ('11111111111')
                            try:
                                # print('3333')
                                appurl = 'http://sj.qq.com/myapp/detail.htm?apkName=' + pkgName
                                app_content = requests.get(appurl, headers=headers).text
                                soup = bs4.BeautifulSoup(app_content)
                                category = soup.find_all(class_='det-type-box')[0].a.text
                                detail = soup.find_all(class_='det-app-data-info')[0].text
                                # print (detail)
                                des = re.sub('\n', ' ', detail)
                                des = re.sub('\r', ' ', des)
                                des = re.sub(',', ' ', des)
                                # print (appName)
                                appData = {}
                                appData['kws'] = key_word
                                appData['categories'] = category
                                appData['details'] = des
                                appData['source'] = 'QQ'
                                # print(appData)

                                # print('from疼讯，' + appName + '入库')

                                self.q.appDes.set(appData,len(key_word))
                                self.q.data.delete(key_word)
                                Flag = True
                                break;


                            except:
                                # self.q.queueQQ.set(key_word, value)
                                break;
                    if Flag is False:
                        # print('？？？？？？')
                        # print(key_word,value)
                        self.q.queueQQ.set(key_word,value)
                        self.q.data.delete(key_word)


                    # print('last')

            else:
                break;

        print ('QQ:over...')
        self.q.flag_360 = True


if __name__ == '__main__':

    d = database_list.database()
    t1 = ConsumerQQ(d)
    t1.start()