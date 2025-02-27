class entUrlResult(object):
    rlt=dict(key=0,value=None)
    rlt = {"url": '', "title": '', "html":'' , "urllist":''}

    def __new__(self, url, title,html,urllist):
        # url,title,html,urllist
        self.rlt["url"] = url
        self.rlt["title"] = title
        self.rlt["html"] = html
        self.rlt["urllist"] = urllist
        return self.rlt