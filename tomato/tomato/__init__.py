import pymysql
from libs.orm import patch_model
#Django框架加载前

pymysql.install_as_MySQLdb()
patch_model()     #为ORM增加缓存处理
