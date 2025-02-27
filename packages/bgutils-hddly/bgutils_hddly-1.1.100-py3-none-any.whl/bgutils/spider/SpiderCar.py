from dataclasses import dataclass
from datetime import datetime

from bgutils import dtUtil
from bgutils.spider.BaseSpider import BaseSpider

@dataclass
class SpiderCar(BaseSpider):
    title: str #小车名称2
    style: str #小车类型3
    engine: str #发动机类型 4
    desc: str #书描述
    price: str #车价
    pic: str #车图片1
    regdate: str #注册日期
    distance: str #行驶路程
    score: str #口碑分 3
    color: str #车身颜色
    pricecount: str #价格条数


    def __init__(self, username, collector, rawurl, rawdata):
        super().__init__(username, collector, "car_data", rawurl, rawdata)
        return
