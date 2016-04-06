import threading
import codecs
import pandas as pd
import database_list
import time


class Insertdata(threading.Thread):
    def __init__(self, database):
        super().__init__()
        threading.Thread.__init__(self)
        self.q = database

    def run(self):
        print ('Insertdata:starting...')



        while True:
            appData = {'kws': '', 'categories': '', 'details': '', 'source': ''}
            appData = {key: [] for key in appData}
            deleteData =[]

            if self.q.flag_QQ is False or self.q.flag_baidu is False or self.q.flag_360 is False or len(self.q.appDes.keys()) !=0:

                appkey = list(self.q.appDes.keys())
                # print(len(appkey))
                # print (appDes.qsize())
                for app in appkey:

                    # print (type(appDes))
                    appDes = eval(app)
                    # value = self.q.appDes.get(appDes)
                    # appDes = self.q.appDes.get()
                    # print('数据：%s' % (len(value)))
                    appData['kws'].append(appDes['kws'])

                    appData['categories'].append(appDes['categories'])
                    appData['details'].append(appDes['details'])
                    appData['source'].append(appDes['source'])
                    # print ('数据：%s' % (len(appData['kws'])))
                    # print(appData)
                    deleteData.append(app)
                    # print (len(appData['kws']))

                # print(len(appData['kws']))
                    if len(appData['kws']) % 1000 == 0:
                        # time.sleep(7)
                        # print('appData')
                        appData_all = pd.DataFrame(appData)
                        col = [ 'kws','categories', 'details',  'source']
                        appData_all = appData_all[col]
                        appData_all.to_csv('../app_data/appDes.csv', mode='a', encoding='utf-8', index=None, header=None)

                        # 插入完成删除数据库中的app
                        # print (appData['kws'])
                        # print (self.database.redisdata)
                        self.q.appDes.delete(*deleteData)
                        # self.q.data.delete(*appData['kws'])

                        appData = {key: [] for key in appData}
                        print('1000条完成')
               	#         time.sleep(100)
            else:
                break;
        print('Insertdata:over...')

class Nodesapp(threading.Thread):
    def __init__(self, database):
        super().__init__()
        threading.Thread.__init__(self)

        self.q = database

    def run(self):
        print ('Nodesapp: staring...')
        # sleep(12)
        while True:
            if self.q.flag_over is False or len(self.q.queueNodes.keys()) != 0:
            
                for unfindApp in self.q.queueNodes.keys():

                        # print ('::::::'+unfindApp)
                        f = codecs.open('../app_data/nofind.csv', 'a','utf-8')
                        f.write(unfindApp + '\n')
                        self.q.queueNodes.delete(unfindApp)
                       # time.sleep(3)
              #  print('1000条没找到。。。')
                                # time.sleep(5)
            else:
                break;
        print ('Nodesapp:over...')
if __name__ == '__main__':
    d = database_list.database()
    t1 = Insertdata(d)
    t2 = Nodesapp(d)
    t1.start()
    t2.start()
