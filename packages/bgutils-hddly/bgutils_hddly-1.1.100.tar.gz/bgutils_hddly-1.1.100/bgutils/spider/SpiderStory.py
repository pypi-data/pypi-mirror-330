from dataclasses import dataclass
from datetime import datetime

from bgutils import dtUtil
from bgutils.spider.BaseSpider import BaseSpider

@dataclass
class SpiderStory(BaseSpider):
    title: str #故事标题
    author: str #故事作者
    link: str #故事详情链接
    desc: str #故事描述
    content: str #故事内容
    pic: str #故事图片

    def __init__(self, username, collector, rawurl, rawdata):
        super().__init__(username, collector, "storys_data", rawurl, rawdata)
        return
