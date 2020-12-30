import os

#Redis 配置
REDIS = {
    "host":"172.18.0.20" if "SWIPER_DOCKER" in os.environ else "localhost",
    "port":6379,
    "db":6,
}


# 云之讯短信平台配置
YZX_SMS_API = 'https://open.ucpaas.com/ol/sms/sendsms'
YZX_SMS_ARGS = {
    "sid": '4ad2912058ef9ef9ea0cdd790e0f7361',
    "token": 'cc2de93f90e7356abf9580a7de00074b',
    "appid": '3a34537ffb294f0a8af45555a161e68a',
    "templateid": '527103',
    "param": None,
    "mobile": None
}


# 七牛云配置
QN_ACCESSKEY = "UYa9TK0V-wLabVW7ev5gqZWnXsRb1q6LBh494T3C"
QN_SECRETKEY = "eacCN0qLKU7wWyMPLioqxiKB81oz58hd7UTxu-3N"
QN_BUCKET = "tomotolux"
QN_BASE_URL = "http://ql25nwi7a.hn-bkt.clouddn.com"
