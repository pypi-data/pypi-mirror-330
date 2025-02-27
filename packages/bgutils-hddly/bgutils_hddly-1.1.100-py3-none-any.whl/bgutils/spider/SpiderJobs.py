from dataclasses import dataclass
from datetime import datetime

from bgutils.spider.BaseSpider import BaseSpider

@dataclass
class SpiderJobs(BaseSpider):
    job_name: str #职位名称，如"大数据开发"
    job_Id: str #职位ID,如"143759451"
    job_url: str #职位链接，如"https://jobs.51job.com/qingdao/143759451.html?s=sou_sou_soulb&t=0_0&re…"
    company_name :str #招聘企业，如"青岛某科技信息有限公司"
    release_time :str #职位发布晶时间，如"2023-05-22 09:26:08"
    job_salary: str #薪资 "7千-1.4万"
    job_address: str #工作地点,如"青岛"
    work_year: str #工作年限要求,如    "无需经验"
    degree_request:str #工作学历要求，如 "本科"
    job_explain: str #经验要求，如"无需经验,hadoop,java,hive,数据库,数据分析,…"

    def __init__(self, username, collector, rawurl, rawdata):
        super().__init__(username, collector, "jobs_data", rawurl, rawdata)
        return
