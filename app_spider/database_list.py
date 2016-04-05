import redis


class database():
    def __init__(self):
        self.data = redis.StrictRedis(host='127.0.0.1', port=6379, db='1', charset='utf8', decode_responses=True)
        self.appDes = redis.StrictRedis(host='127.0.0.1', port=6379, db='2', charset='utf8', decode_responses=True)
        self.queueQQ = redis.StrictRedis(host='127.0.0.1', port=6379, db='3', charset='utf8', decode_responses=True)
        self.queue360 = redis.StrictRedis(host='127.0.0.1', port=6379, db='4', charset='utf8', decode_responses=True)
        self.queueBaidu = redis.StrictRedis(host='127.0.0.1', port=6379, db='5', charset='utf8', decode_responses=True)
        self.queueNodes = redis.StrictRedis(host='127.0.0.1', port=6379, db='6', charset='utf8', decode_responses=True)

        self.flag_QQ = False
        self.flag_baidu = False
        self.flag_360 = False
        self.flag_Baidu_spider = False
        self.flag_over = False


