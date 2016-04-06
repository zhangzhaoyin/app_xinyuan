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
import  database_list

class ConsumerBaidu(threading.Thread):
    def __init__(self,database):
        super().__init__()
        threading.Thread.__init__(self)
        self.q = database

    def run(self):
        print ('Baidu:starting...')
        while True:

            if self.q.flag_baidu is False or len(self.q.queue360.keys()) != 0:
                for key_word in self.q.queue360.keys():
                    Flag = False
                    value = self.q.queue360.get(key_word)
                    # print (key_word)
                    try:
                        # print('百度市场')
                        # key_word = self.q.queue360.get()
                        url = 'http://shouji.baidu.com/s?wd=' + key_word
                        response = requests.get(url).text
                        # 获取源码
                        soup = bs4.BeautifulSoup(response)
                        content = soup.find_all('div', class_='top')
                    except:
                        self.q.queueBaidu.set(key_word,value)
                        self.q.queue360.delete(key_word)
                        continue;

                    for i in range(0, len(content)):
                        childcontent = content[i]
                        appName = str(childcontent.a.text)
                        appName = appName.strip()
                        pkgName = childcontent.a['href']
                        if appName == key_word:
                            try:
                                # 拼出app的主页
                                appurl = 'http://shouji.baidu.com' + pkgName
                                # print appurl
                                response1 = requests.get(appurl).text
                                soup1 = bs4.BeautifulSoup(response1)
                                # j解析app的分类标签及描述内容
                                category = soup1.find('div', class_='app-nav').find_all('span')[2].text.strip()
                                des = soup1.find('div', class_='brief-long').find_all('p')[0].text
                                appData = {}
                                # print (appName)
                                appData['kws'] = appName
                                appData['categories'] = category
                                appData['details'] = des
                                appData['source'] = 'baidu'
                                self.q.appDes.set(appData, key_word)
                                self.q.queue360.delete(key_word)

                               # print('from百度市场' + appName + '入库。。。')
                                # print('入库')
                                Flag = True
                                break;

                            except:
                                break;

                    if Flag is False:
                        # print('next')
                        self.q.queueBaidu.set(key_word, value)
                        self.q.queue360.delete(key_word)

            else:
                break;
        print ('Baidu:over...')
        self.q.flag_Baidu_spider = True


if __name__ == '__main__':
    while True:
        try:
            d = database_list.database()
            t1 = ConsumerBaidu(d)
            t1.run()
        except:
            continue;

