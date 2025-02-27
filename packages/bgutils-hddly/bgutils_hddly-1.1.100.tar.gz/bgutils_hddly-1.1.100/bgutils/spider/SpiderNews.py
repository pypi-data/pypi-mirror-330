from dataclasses import dataclass
from datetime import datetime
from bgutils.spider.BaseSpider import BaseSpider

@dataclass
class SpiderNews(BaseSpider):
    newsTitle: str #新闻标题
    newsUrl: str #新闻地址url
    ctime: str  #新闻发布时间
    media_name: str #发布媒体
    keywords: str #关键词

    def __init__(self, username, collector, rawurl, rawdata):
        super().__init__(username, collector, "news_data", rawurl, rawdata)
        return

