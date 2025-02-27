from datetime import datetime

DATETIMEFORMT="%Y-%m-%d %H:%M:%S"
def formatted_time(my_time):
    return my_time.strftime(DATETIMEFORMT)

def formatted_now():
    return datetime.now().strftime(DATETIMEFORMT)
#  self.coll_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') #采集时间，实体初始方法自动填充