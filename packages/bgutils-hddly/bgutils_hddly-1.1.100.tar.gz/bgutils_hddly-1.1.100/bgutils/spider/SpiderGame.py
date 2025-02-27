from dataclasses import dataclass
from datetime import datetime

from bgutils.spider.BaseSpider import BaseSpider

@dataclass
class SpiderGame(BaseSpider):
    id: str #游戏ID
    title: str #游戏标题
    playlink: str #游戏地址
    introduce: str #游戏介绍
    pic : str #游戏图片地址

    def __init__(self, username, collector, rawurl, rawdata):
        super().__init__(username, collector, "games_data", rawurl, rawdata)
        return


