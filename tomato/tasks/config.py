broker_url = "redis://127.0.0.1:6379/6"
broker_pool_limit = 10                     #Borker 连接池，默认是10

timeone = "Asia/Shanghai"                  #时区
accept_content = ["pickle"]
task_serializer = "pickle"


result_expires =3600                        #任务结束过期时间
result_backend = "redis://127.0.0.1:6379/6"
result_serializer = "pickle"
result_cache_max = 10000                     #任务最大缓存数量

worker_redirect_stdoyts_level = "INFO"