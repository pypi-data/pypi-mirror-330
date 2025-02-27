from dataclasses import dataclass
from datetime import datetime

from bgutils.spider.BaseSpider import BaseSpider

@dataclass
class SpiderData(BaseSpider):
    id: str
    title: str
    url: str
    price: str
    pic: str
    time_sort: str

    def __init__(self, username, collector, rawurl, rawdata):
        super().__init__(username, collector, "goods_data", rawurl, rawdata)
        return

