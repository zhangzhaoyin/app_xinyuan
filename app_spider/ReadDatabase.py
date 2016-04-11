import redis
import pandas as pd
import SendEmail
import database_list


class insertData():
    def __init__(self,filename,database):
        self.host =  '127.0.0.1'
        self.port = 6379
        self.filename = filename
        self.database = database

    def connection(self):
        self.redis = redis.StrictRedis(host='127.0.0.1', port=6379, db='1', charset='utf8', decode_responses=True)
        # self.conn = redis.ConnectionPool(self.host, self.port, db='app')
        # self.redis = redis.Redis(connection_pool=self.conn)
        print ('连接redis成功...')

    def execute(self):
        # batch_size = 10000
        pipeline_redis = self.redis.pipeline()
        try:
            kwlist = pd.read_csv(self.filename, header=None, encoding='utf8').dropna()
            kwlist = kwlist.reset_index(level=1)
            for k in kwlist.values:
                value = k[0]
                key = k[1].strip().lower()
                # print (value)
                pipeline_redis.set(key, value)

            pipeline_redis.execute()
            print('入库成功...')
            self.database.flag_QQ = True
            print (self.database.flag_QQ)
        except:
            s =SendEmail.sendEmail()
            s.readConfig()
            s.send_mail(s.recipients,s.error1)
            print ('数据异常')




    def run(self):
        self.connection()
        self.execute()

if __name__ == '__main__':
    d = database_list.database()
    data = insertData('../app_data/kw.csv',d)
    data.run()

