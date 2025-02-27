from dataclasses import dataclass
from datetime import datetime
from bgutils.spider.BaseSpider import BaseSpider
@dataclass
class SpiderHouse(BaseSpider):
    title: str #房产标题
    addr: str  #地址
    houseinfo: str #房屋信息
    houseurl: str #房屋url
    price : str #房总价
    unitprice : str #房单价
    img : str #图片
    city : str  # 所在城市

    def __init__(self, username, collector, rawurl, rawdata):
        super().__init__(username, collector, "house_data", rawurl, rawdata)
        return





