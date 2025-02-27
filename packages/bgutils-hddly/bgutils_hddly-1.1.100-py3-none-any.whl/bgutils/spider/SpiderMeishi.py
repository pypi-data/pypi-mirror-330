from dataclasses import dataclass
from datetime import datetime

from bgutils.spider.BaseSpider import BaseSpider

@dataclass
class SpiderMeishi(BaseSpider):
    uid: str #商品ID
    author: str #作者
    title: str #商品标题
    mainingredient: str #原材料
    dateline :str #日期
    subject:str #主题
    url: str #商品url
    pic: str #商品的图片url,对应fcover

    def __init__(self, username, collector, rawurl, rawdata):
        super().__init__(username, collector, "meishi_data", rawurl, rawdata)
        return

