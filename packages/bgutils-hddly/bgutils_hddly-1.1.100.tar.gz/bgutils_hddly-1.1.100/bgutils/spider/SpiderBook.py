from dataclasses import dataclass
from datetime import datetime

from bgutils import dtUtil
from bgutils.spider.BaseSpider import BaseSpider


@dataclass
class SpiderBook(BaseSpider):
    title: str #书标题
    author: str #书作者
    link: str #书详情链接
    desc: str #书描述
    price: str #书单价
    pic: str #图片

    def __init__(self, username, collector, rawurl, rawdata):
        super().__init__(username, collector, "books_data", rawurl, rawdata)

