from dataclasses import dataclass
from datetime import datetime

from bgutils.spider.BaseSpider import BaseSpider

@dataclass
class SpiderVideo(BaseSpider):
    id: str  #视频ID,如"222666"
    typename: str #视频分类
    title: str  #视频标题,如"生死狙击之僵尸前线"
    playlink: str #视频播放地址
    pic: str #视频图片地址
    duration: str #视频播放时长
    introduce: str #视频介绍，如 "全新变异体-月兔精上线"


    def __init__(self, username, collector, rawurl, rawdata):
        super().__init__(username, collector, "videos_data", rawurl, rawdata)
        return
