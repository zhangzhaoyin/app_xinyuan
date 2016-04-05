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



class ConsumerBaiduspider(threading.Thread):
    def __init__(self,database):
        super().__init__()
        threading.Thread.__init__(self)
        self.q = database
        # self.appDes = appDes

    def run(self):

        print ('Baiduspider:starting...')
        header = {
            'Host': 'baidu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240',
        }
        Cookies = []
        bdurl = 'http://www.baidu.com'
        bd = requests.get(bdurl, headers=header)
        cookie = bd.cookies
        Cookies.append(cookie)
        while True:
            if self.q.flag_Baidu_spider is False or len(self.q.queueBaidu.keys()) != 0:
                for key_word in self.q.queueBaidu.keys():
                    value =self.q.queueBaidu.get(key_word)
                    # print(key_word)

                    try:
                        # print('百度搜索')
                        # key_word = self.q.queueBaidu.get()
                        # print ('1')
                        url = 'http://www.baidu.com/s?wd=' + key_word
                        r = requests.get(url, headers=header, cookies=Cookies[0])
                        Cookies = []
                        Cookies.append(r.cookies)
                        html = r.text
                        soup = bs4.BeautifulSoup(html)
                        r.close()
                        # print (soup)
                        error = soup.find_all('div', class_='nors')
                        if error:
                            self.q.queueBaidu.delete(key_word)
                            self.q.queueNodes.set(key_word,value)
                            continue;

                    except:
                        self.q.queueNodes.set(key_word,value)
                        self.q.queueBaidu.delete(key_word)
                        continue;

                    dict_all = {}
                    dict_description = {}
                    description = []
                    dict_rs = {}
                    rs = []

                    # 搜索标题和摘要
                    titles = soup.find_all('div', class_='c-tools')
                    abstract = soup.find_all('div', class_='c-abstract')
                    for s, c in zip(titles, abstract):
                        # s=str(s['data-tools'])
                        # s=s.replace('\\','')
                        # print s
                        try:
                            s = s['data-tools']
                            dictinfo = json.loads(s)
                        except:
                            print('error.....')
                            # sleep(100)
                            # count +=1
                            # count=str( count)
                            # open(u'count.txt','w').write(count+'\n')

                            continue;

                        title = dictinfo["title"].strip()

                        con = c.get_text().strip()
                        # print con
                        dict_description['title'] = title
                        dict_description['abstract'] = con
                        # print dict_description
                        description.append(dict_description.copy())
                    # 相关软件和软件名字
                    rs_title = soup.find_all('div', class_='opr-recommends-merge-content')
                    rs_content = soup.find_all('div', class_='c-row c-gap-top')
                    if rs_title and rs_content:
                        rs_title = rs_title[0].find_all('div', class_='cr-title c-clearfix')

                        for r, o1 in zip(rs_title, rs_content):
                            con = []
                            for s in r.find_all('span'):
                                if 'title' in s.attrs:
                                    title_R = s['title'].strip()
                                    # print title_R
                                    dict_rs['rs_title'] = title_R
                            # for o1  in rs_content:
                            o2 = o1.find_all('div', class_='c-gap-top-small')
                            # 	#print '--------------------------------------------------'

                            for o in o2:
                                if len(o.a.get_text()) != 0:
                                    content = o.a.get_text().strip()
                                    # print content
                                    con.append(content)
                            dict_rs['rs_content'] = con
                            # print dict_rs
                            rs.append(dict_rs.copy())
                    else:
                        rs = []

                    if len(description) != 0 or len(rs) != 0:
                        appData = {'kws': '','categories':'', 'details': '', 'source':''}
                        appData = {key: [] for key in appData}
                        # print (key_word)
                        source = 'baiduSpider'
                        category ='0'

                        # dict_all['related_software'] = rs
                        appData['kws'].append(key_word)
                        # dict_all['kw'] = key_word + '下载'
                        appData['details'].append(description + rs)
                        appData['source'].append(source)
                        appData['categories'].append(category)

                        if len(appData['kws']) % 1 == 0:
                            col = ['kws', 'categories', 'details', 'source']
                            # col = ['kws', 'details', 'source']
                            appData_all = pd.DataFrame(appData)
                            appData_all =appData_all[col]
                        #    print('ok')
                            appData_all.to_csv('data/appDes.csv', mode='a', encoding='utf-8', index=None, header=None)

                            # appData_all.to_csv('data/appBaiduSpider.csv', mode='a', encoding='utf-8', index=None, header=None)
                            # print('from百度搜索' + key_word + '入库。。。')
                            self.q.queueBaidu.delete(*appData['kws'])
                            # self.q.data.delete(key_word)
                            # print dict_all
                            # line = json.dumps(dict_all.copy(), ensure_ascii=False)
                            # print (line)

                            # open('app_baiduspider.json', 'a').write(line + '\n')
                    else:
                        # noDes = key_word

                        self.q.queueNodes.set(key_word,value)
                        self.q.queueBaidu.delete(key_word)
                        continue;
                        # open(u'noDes.txt', 'a').write(noDes + '\n')

            else:
                break;
        print ('Baiduspider:over...')
        self.q.flag_over = True


if __name__ == '__main__':
    d = database_list.database()

    t1 = ConsumerBaiduspider(d)
    t1.start()
