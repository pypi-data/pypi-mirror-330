import json

import pandas as pd
import pymysql

from bgutils.redisUtil import redisUtil

db_config = {
    "host": "home.hddly.cn",
    "port": 53306,
    "user": "test",
    "password": "test",
    "db": "test",
    "charset": "utf8mb4"
}
class mysqlUtil:
    __redis = redisUtil()
    __connection= None

    def __init__(self):
        return

    def OpenDB(self):
        if not self.__connection:
            self.__connection = pymysql.connect(**db_config)
        return self.__connection



    # 查询上传文件是否有重复
    # def chk_file_exist(self, fdesc, fsize, duration):
    #     if fsize and duration:
    #         # 判断float相等： abs(duration-123.31)<0.01
    #         sql = "select id from sftp_files where fsize={} and  abs(duration-{})<0.01 limit 1".format(fsize, duration)
    #         connection = self.engine.connect()
    #         df = pd.read_sql(sql, con=connection)
    #         results = json.loads(df.to_json(orient='records'))
    #         if results and len(results) == 1:
    #             # 记录采集重复信息
    #             sys.stdout.write("repeat:" + fdesc + "," + str(fsize) + "," + str(duration) + "\n")
    #             return 1
    #         else:
    #             return 0
    #     else:
    #         return -1

    # def chk_file_exist_surl(self, surl, fdesc):
    #     if surl and fdesc:
    #         surl = surl[0:499]  # 只取前499位
    #         fdesc = fdesc[0:999]
    #         # 先从redis中判断 是否存在，如果不存在，再从mysql中查找，找到的话添加到redis中
    #         if self.__redis.sismember("surl", surl):
    #             return 1
    #         if self.__redis.sismember("fdesc", fdesc):
    #             return 1
    #
    #         # 判断float相等： abs(duration-123.31)<0.01
    #         sql = "select id from sftp_files where surl='{}' or fdesc='{}' limit 1".format(surl, fdesc)
    #         connection = self.engine.connect()
    #         df = pd.read_sql(sql, con=connection)
    #         results = json.loads(df.to_json(orient='records'))
    #         if results and len(results) == 1:
    #             # 记录采集重复信息
    #             self.__redis.sadd("surl", surl)
    #             self.__redis.sadd("fdesc", fdesc)
    #             return 1
    #         else:
    #             return 0
    #     else:
    #         return -1

    # 添加上传文件记录
    def sftp_file_ins(self, filename, url, stud, fdesc, fsize, duration, ftype, pid, surl):
        try:
            surl = surl[:499]
            query = ("insert into sftp_files (filename,url,stud,fdesc,fsize,duration,ftype,pid,surl) VALUES (%s, %s, "
                     "%s, %s, %s, %s, %s, %s, %s)")
            parameters = (filename, url, stud, fdesc, fsize, duration, ftype, pid, surl)
            cursor = self.__connection.cursor()
            cursor.execute(query, parameters)
            self.__connection.commit()
            cursor.close()
        except Exception as ex:
            print("sftp_file_ins error:%s" % ex)

    # 获了上传文件记录
    def get_file_list(self, ftype):
        if ftype:
            ftype = str(ftype).lower()
            sql = 'select id,url,fdesc,fsize,duration,ftype,uptime,pid from sftp_files where ftype="{}" order by uptime desc limit 100'.format(
                ftype)
        else:
            ftype = ".mp4"
            sql = 'select id,url,fdesc,fsize,duration,ftype,uptime,pid from sftp_files where ftype="{}" order by uptime desc limit 100'.format(
                ftype)
        connection = self.OpenDB()
        df = pd.read_sql(sql, con=connection)
        results = json.loads(df.to_json(orient='records'))
        if results and len(results) == 1:
            return results[0]
        elif results and len(results) > 1:
            return results
        else:
            return None
        # 获了上传文件记录

    def get_files_bypid(self, pid):
        if pid:
            pid = str(pid).lower()
            sql = 'select id,url,fdesc,fsize,duration,ftype,uptime,pid from sftp_files where pid="{}" order by id desc limit 100'.format(
                pid)
        else:
            pid = "p023101".lower()
            sql = 'select id,url,fdesc,fsize,duration,ftype,uptime,pid from sftp_files where pid="{}" order by id desc limit 100'.format(
                pid)
        connection = self.OpenDB()
        df = pd.read_sql(sql=sql, con=connection)
        results = json.loads(df.to_json(orient='records'))
        if results and len(results) == 1:
            return results[0]
        elif results and len(results) > 1:
            return results
        else:
            return None

    # def process_item(self, item, tblname):
    #     data = pd.DataFrame(dict(item), index=[0])
    #     data.to_sql(tblname, self.engine, if_exists='append', index=False)  # 'taobao_data'
    #     return item

    def escape(self, content):
        if content and (len(content) > 0) and (len(str(content).strip()) > 0):
            content = content.replace("\\\\", "\\\\\\\\");
            content = content.replace("_", "\\\\_");
            content = content.replace("%", "\\\\%");
            content = content.replace("'", "\\\\'");

        return content;
