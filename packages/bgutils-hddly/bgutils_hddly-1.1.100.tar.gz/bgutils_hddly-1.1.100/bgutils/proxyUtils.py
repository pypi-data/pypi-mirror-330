import json
import random

import pandas as pd
from bgutils.redisUtil import redisUtil

agents={}
def select_rand_db(self, types=None):
    if types:
        sql = "select ip,port,types from eie_ip where types='{}' order by rand() limit 1".format(types)
    else:
        sql = "select ip,port,types from eie_ip order by rand() limit 1 "
    df = pd.read_sql(sql, self.engine)
    results = json.loads(df.to_json(orient='records'))
    if results and len(results) == 1:
        return results[0]
    return None

def getagent():
    redis= redisUtil()
    global  agents
    agents=redis.hgetall('scrapy:agent')
    random_item = random.choice(list(agents.items()))
    proxy = random_item[1].decode('utf-8').lower()
    return proxy