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
import multiprocessing
import database_list

class Consumer360(threading.Thread):
    def __init__(self,database):
        super().__init__()
        threading.Thread.__init__(self)
        self.q = database

    def run(self):
        print ('360:starting...')
        while True:

            if self.q.flag_360 is False or len(self.q.queueQQ.keys()) != 0:
                for key_word in self.q.queueQQ.keys():
                    Flag = False
                    value = self.q.queueQQ.get(key_word)
                    try:
                        # key_word = self.q.queueQQ.get()
                        url = 'http://zhushou.360.cn/search/index/?kw=' + key_word
                        response = requests.get(url).text
                        soup = bs4.BeautifulSoup(response)
                        content = soup.find_all('div', class_='SeaCon')[0].find_all('h3')
                    except:
                        self.q.queue360.set(key_word,value)
                        self.q.queueQQ.delete(key_word)
                        continue;
                    for i in range(0, len(content)):

                        childcontent = content[i]
                        appName = childcontent.a['title'].lower()
                        pkgName = childcontent.a['href']
                        if appName == key_word:
                            try:
                                # print('1111')
                                appUrl = 'http://zhushou.360.cn' + pkgName
                                response = requests.get(appUrl).text
                                soup = bs4.BeautifulSoup(response)
                                des = soup.find_all('div', class_='breif')[0].text.strip()
                                des = str(des)
                                des = des.replace('\r\n', '')
                                if len(soup.find_all('div', class_='app-tags')) != 0:
                                    # print '-------------'
                                    app_tags = soup.find('div', class_='app-tags').find_all('a')

                                    # print type(app_tags)
                                    category = []
                                    for app_tag in app_tags:
                                        a = app_tag.text.strip()  # .encode('utf-8')
                                        category.append(a)
                                    # print appName
                                    # print category+des
                                    appData = {}
                                    appData['kws'] = appName
                                    appData['categories'] = category
                                    appData['details'] = des
                                    appData['source'] = '360'
                                    # print(appName)

                                    self.q.appDes.set(appData, key_word)
                                    self.q.queueQQ.delete(key_word)
                                    # print('from360,' + appName + '入库。。。')
                                    # print ('入库')
                                    Flag = True
                                    break;

                                else:
                                    # 解析出app的分类和描述信息
                                    # print (appName)
                                    appData['kws'] = appName
                                    appData['categories'] = 0
                                    appData['details'] = des
                                    appData['source'] = '360'
                                    # print('from360,' + appName + '入库。。。')
                                    # print('入库')
                                    self.q.appDes.set(appData, key_word)
                                    self.q.queueQQ.delete(key_word)
                                    Flag = True
                                    break;

                            except:
                                break;
                    if Flag is False:
                        # print('next')
                        self.q.queue360.set(key_word, value)
                        self.q.queueQQ.delete(key_word)

            else:
                break;
        print ('360:over...')
        self.q.flag_baidu = True

if __name__ == '__main__':
    d = database_list.database()

    t1 = Consumer360(d)
    t1.start()

