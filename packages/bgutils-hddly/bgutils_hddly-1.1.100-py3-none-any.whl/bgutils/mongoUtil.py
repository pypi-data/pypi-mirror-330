
import pymongo
from bgutils import dtUtil
from pymongo import MongoClient
import dateutil.parser

class mongoUtil:
    __mongo_ip="home.hddly.cn"
    __port="57017"
    __urlendstr="/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false"

    def __init__(self):
        self.collection = None

    def OpenDB(self, dbname):
        self.__mongo_ip = "home.hddly.cn"
        self.__port = "57017"
        uri = "mongodb://"+self.__mongo_ip+":" + self.__port + self.__urlendstr
        self.con = MongoClient(uri, connect=False)
        self.db = self.con[dbname]

    def OpenDBYgxy(self, dbname):
        self.__mongo_ip = "10.255.10.52"
        self.__port = "27017"
        uri = "mongodb://" + self.__mongo_ip + ":" + self.__port + self.__urlendstr
        self.con = MongoClient(uri, connect=False)
        self.db = self.con[dbname]

    def OpenDBAny(self, ip,port,dbname):
        self.__mongo_ip = ip
        self.__port = port
        uri = "mongodb://" + self.__mongo_ip + ":" + self.__port + self.__urlendstr
        self.con = MongoClient(uri, connect=False)
        self.db = self.con[dbname]

    def OpenDBUri(self, dburi,dbname):
        self.con = MongoClient(dburi, connect=False)
        self.db = self.con[dbname]

    def closeDB(self):
        self.con.close()

    def process_item(self, item, collection):
        jsontmp = dict(item)
        self.collection = self.db[collection]
        self.collection.insert_one(jsontmp)
        return item

    def process_items(self, items, collection):
        self.collection = self.db[collection]
        self.collection.insert_many(items)
        return items
    # def process_items(self, items, collection):
    #     docs = []
    #     for item in items:
    #         jsontmp = dict(item)
    #         docs.append(jsontmp)
    #     if len(docs) > 0:
    #         self.collection = self.db[collection]
    #         self.collection.insert_many(docs)
    #     return items
    def process_items_collect_time(self, items, collection):
        docs = []
        for item in items:
            jsontmp = dict(item)
            coll_time= jsontmp['coll_time']
            parsed_date = dateutil.parser.parse(coll_time)
            jsontmp['coll_time']=parsed_date
            # jsontmp['coll_time']=dtUtil.formatted_time(parsed_date)
            docs.append(jsontmp)
        if len(docs) > 0:
            self.collection = self.db[collection]
            self.collection.insert_many(docs)
        return items

    def get_db_count(self, collection, collector):
        self.collection = self.db[collection]
        rowcount = self.collection.count_documents({'collector': collector})
        return {'collector': collector, 'collcount': rowcount}

    def get_db_count_all(self, collection):
        self.collection = self.db[collection]
        cur = self.collection.aggregate([
            {"$group": {"_id": "$collector", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ])
        # $group操作符去利用一个指定的键进行分组
        # $collector - key
        # $sum累加器进行文档的统计计算
        # $sort 排序
        counts = dict()
        for document in cur:
            # 'ascii' codec can't encode characters in position 0-2: ordinal not in range(128) ,
            # 。你可以使用Python的type()函数来检查数据类型，以及使用.encode('utf-8')和.decode('utf-8')来显式转换编码
            try:
                if document['_id'] and document['count']:
                    collecter = document['_id']
                    counts[collecter] = document['count']
                # print(document['_id'] + '\t' + str(document['count']))
            except Exception as ex:
                print("get_db_count_all" + str(ex) + ",document:" + str(document))
        return counts

    def set_db_index(self):
        self.db['users'].create_index([('id', pymongo.ASCENDING)])
        self.db['weibos'].create_index([('id', pymongo.ASCENDING)])

    def insertMongdbOne(self,collection, jsoninfo):
        self.collection = self.db[collection]
        print(jsoninfo)
        self.collection.insert_one(jsoninfo)

if __name__ == '__main__':

    mongo = mongoUtil()
    mongo.OpenDB("pythondb")

    mongo.closeDB()
    exit()
