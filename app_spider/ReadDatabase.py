import redis
import pandas as pd


class insertData():
    def __init__(self,filename):
        self.host =  '127.0.0.1'
        self.port = 6379
        self.filename = filename

    def connection(self):
        self.redis = redis.StrictRedis(host='127.0.0.1', port=6379, db='1', charset='utf8', decode_responses=True)
        # self.conn = redis.ConnectionPool(self.host, self.port, db='app')
        # self.redis = redis.Redis(connection_pool=self.conn)
        print ('连接redis成功...')

    def execute(self):
        # batch_size = 10000
        pipeline_redis = self.redis.pipeline()

        kwlist = pd.read_csv(self.filename, header=None).dropna()
        # print (kwlist)
        kwlist = kwlist.reset_index(level=1)
        for k in kwlist.values:
            value = k[0]
            key = k[1].strip().lower()
            # print (value)
            pipeline_redis.set(key, value)

        pipeline_redis.execute()
        print ('入库成功...')


    def run(self):
        self.connection()
        self.execute()

if __name__ == '__main__':
    data = insertData('./data/kw.csv')
    data.run()
