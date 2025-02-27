import os

import paramiko
from bgutils.redisUtil import redisUtil
from moviepy.video.io.VideoFileClip import VideoFileClip

from bgutils.mysqlUtil import mysqlUtil

class ftpUtil:
    # 登陆参数设置
    __hostname = "home.hddly.cn"
    __host_port = 18030
    __username_stud ="student"
    __password_stud ="student123.com"
    __remotedir_stud = "send/"
    __url_head="http://home.hddly.cn:8081/media/family_student/send/"
    __mreids = redisUtil()

    def chk_file_exist_surl(self,surl,fdesc):
        return self.__mutil.chk_file_exist_surl(surl,fdesc)

    def putfile_project(self, local_path, prj_id, stud_id, no_file,fdesc,surl):
        # # 要传输文件的路径
        # filepath = "./myname.jpg"
        # # 上传后的传输文件的文件名
        # remote_file = 项目ID(6位)+学生ID（11位）+文件ID(2位)+文件类型
        # 如P22001_20190010011_01.jpg
        try:
            ftype = os.path.splitext(local_path)[-1]
            if ftype.upper()=='.MP4' or ftype.upper()=='.WMV':
                clip=VideoFileClip(local_path)
                duration=clip.duration
            else:
                duration=0
            fsize=os.path.getsize(local_path)
            transport = paramiko.Transport((self.__hostname, self.__host_port))
            transport.connect(username=self.__username_stud, password=self.__password_stud)
            sftp = paramiko.SFTPClient.from_transport(transport)
            pid=prj_id
            remotepath = "%s%s"%(self.__remotedir_stud , pid)
            try:
                sftp.chdir(remotepath)
            except:
                sftp.mkdir(remotepath)
                sftp.chdir(remotepath)
            stud = stud_id
            no = no_file
            remote_file = "%s%s%s%s"%(pid,stud,no,ftype)
            sftp.put(local_path, remote_file)
            print('success upload file......')
            sftp.close()
            transport.close()
        except Exception as ex:
            print("connect error:%s" % ex)

        try:
            # 记录文件列表
            # item = entSftpFile()
            # item['filename'] = local_path
            # item['url'] = self.__url_head+remote_file
            # item['stud'] = stud
            remotefullpath = "%s%s/%s" % (self.__url_head,
                                           pid,
                                           remote_file)
            myutil = mysqlUtil()
            myutil.OpenDB()
            myutil.sftp_file_ins(local_path,
                                       remotefullpath,
                                       stud,
                                       fdesc,
                                       fsize,
                                       duration,
                                       ftype,
                                       pid,
                                       surl)
            print('success insert mysql......')
            key = self.__mreids.getusernamekey(stud_id,self.__mreids.RedisKey.SFTP_FILES_LIST)
            self.__mreids.hset(key,remote_file,remotefullpath)
            print('success insert redis......')

        except Exception as ex:
            print("sftp_file_ins error:%s" % ex)

    def putfile_stud(self,local_path,prj_id,stud_id,no_file):
        self.putfile_project(local_path,prj_id,stud_id,no_file,'','');

