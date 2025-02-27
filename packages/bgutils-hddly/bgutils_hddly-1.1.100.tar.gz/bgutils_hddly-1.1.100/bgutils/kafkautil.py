import logging
from dataclasses import dataclass
from enum import Enum
from flask import json
from flask.json import dumps
from kafka import KafkaProducer, KafkaConsumer

# 非阻塞取消息的间隔（秒）
KAFKA_POLL_INTERVAL = 0.5
def init_kafak():
    global KAFKA_BOOTSTRAP_SERVERS
    KAFKA_BOOTSTRAP_SERVERS = 'home.hddly.cn:9092'
    global KAFKA_TOPIC_NAME  # Kafka主题
    KAFKA_TOPIC_NAME = 'tp_spider'
    global KAFKA_GROUP_ID
    KAFKA_GROUP_ID = 'tp_spider'
    global producer_spider
    producer_spider = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda m: json.dumps(m).encode('utf-8')
    )
    global consumer_spider
    consumer_spider = KafkaConsumer(
        KAFKA_TOPIC_NAME,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset='earliest',  # 从最早的消息开始消费
        enable_auto_commit=True,  # 自动提交偏移量
        group_id=KAFKA_GROUP_ID,  # 消费者组ID，用于协调消费和偏移量管理
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))  # 假设消息是JSON格式
    )

init_kafak()
@dataclass
class EnumUserAction(Enum):
    USER_MENU_CLICK = "user_menu_click"  # 用户登陆的目录
    USER_STUDY_TIME = "user_study_time"  # 学生学习时长


@dataclass
class userData():
    userid: str
    useract: str
    data: str

    def __init__(self, userid, useract, data):
        self.userid = userid
        self.useract = getCommKey(useract)
        self.data = data


def getCommKey(keyname):
    try:
        key = keyname.value
        return key
    except Exception as ex:
        logging.error("error:getcommkey" + str(ex))


def sendKafkaUserAction(current_user, datastrin):
    datastr = userData(str(current_user.user_id), EnumUserAction.USER_MENU_CLICK, datastrin)  # 获取 POST 请求中的 JSON 数据
    return sendKafkaMsg(datastr)


def sendKafkaSpiderData(spiderdata):
    return sendKafkaMsg(spiderdata)


def sendKafkaMsg(datastr):
    # message = json.dumps(datastr).encode('utf-8')  # 将数据转换为 JSON 字符串并编码为字节
    message = json.dumps(datastr) #改在producer_spider中编码
    # 发送消息到 Kafka
    producer_spider.send(KAFKA_TOPIC_NAME, value=message)
    return 1


def getKafkaMsg(current_user):
    # 消费消息
    datas = []
    try:
        # 非阻塞方式
        messages = consumer_spider.poll(timeout_ms=int(KAFKA_POLL_INTERVAL * 1000))
        if messages:
            for topic_part, message_list in messages.items():
                for message in message_list:
                    # 处理消息
                    logging.info(f"Partition: {message.partition}, Offset: {message.offset}, Value: {message.value}")
                    data = message.value
                    datas.append(data)
        # 阻塞方式
        # for message in consumer:
        #     data=message.value
        #     # message是一个ConsumerRecord对象，包含消息的元数据（如偏移量、主题、分区等）和值
        #     print(f"Partition: {message.partition}, Offset: {message.offset}, Value: {message.value}")
        #     datas.append(data)
        return datas
    except Exception as ex:
        logging.error("error:get_message:" + str(ex))
        return None


def close():
    consumer_spider.close()
