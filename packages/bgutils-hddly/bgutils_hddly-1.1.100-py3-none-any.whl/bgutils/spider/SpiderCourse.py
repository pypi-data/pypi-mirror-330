from dataclasses import dataclass
from datetime import datetime

from bgutils import dtUtil
from bgutils.spider.BaseSpider import BaseSpider

@dataclass
class SpiderCourse(BaseSpider):
    title: str #课程标题
    author: str #书作者
    link: str #课程链接
    desc: str #课程描述
    tags: str #标签
    price: str #课程单价
    pic: str #课程图片

    def __init__(self, username, collector, rawurl, rawdata):
        super().__init__(username, collector, "course_data", rawurl, rawdata)
        return
