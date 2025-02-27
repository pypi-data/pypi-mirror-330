from dataclasses import dataclass
from datetime import datetime

from bgutils.spider.BaseSpider import BaseSpider

@dataclass
class SpiderGoods(BaseSpider):
    id: str #商品ID
    title: str #商品标题
    url: str #商品url
    price: str #商品的单价
    pic: str #商品的图片url
    time_sort: str #商品的顺序号

    def __init__(self, username, collector, rawurl, rawdata):
        super().__init__(username, collector, "goods_data", rawurl, rawdata)
        return
