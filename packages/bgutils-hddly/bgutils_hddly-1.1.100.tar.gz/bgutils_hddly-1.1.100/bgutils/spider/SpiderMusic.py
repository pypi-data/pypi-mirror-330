from dataclasses import dataclass
from datetime import datetime

from bgutils.spider.BaseSpider import BaseSpider

@dataclass
class SpiderMusic(BaseSpider):
    id: str  #ID,如"222666"
    song_url: str #歌曲url
    song_name: str  #歌曲名
    artist_url: str #歌手url
    artist_name: str #歌手名
    album_name: str #专辑名
    album_url: str #专辑url

    def __init__(self, username, collector, rawurl, rawdata):
        super().__init__(username, collector, "music_data", rawurl, rawdata)
        return
