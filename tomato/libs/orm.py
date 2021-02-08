from datetime import date
from datetime import time
from datetime import datetime
from django.db import models
from django.db.models.query import QuerySet

from libs.cache import rds
from common.keys import MODEL_K


def get(self,*args,**kwargs):
    """带缓存处理的get 方法"""
    cls_name = self.model.__name__
    # 先检查**kwargs是否存在主键
    pk = kwargs.get("pk") or kwargs.get("id")
    if pk:
        # 从缓存获取数据
        key = MODEL_K % (cls_name,pk)
        model_obj = rds.get(key)
        #检查缓存结果
        if isinstance(model_obj,self.model):
            return model_obj
    #缓存不存在时，调用原 get 接口 从数据库获取
    model_obj = self._get(*args,**kwargs)
    #将数据写入缓存
    key = MODEL_K % (cls_name, model_obj.pk)
    rds.set(key,model_obj)
    return model_obj


def save(self, force_insert=False, force_update=False, using=None,
         update_fields=None):
    # 调用 原save 方法，将数据保存到数据库
    # 将数据保存到缓存
    self._save(force_insert,force_update)
    key = MODEL_K % (self.__class__.__name__,self.pk)
    rds.set(key,self)


def to_dict(self,exclude=()):
    """将Model模型转换成一个字典"""
    attr_dict = {}
    for field in self._meta.fields:
        if field.name in exclude:
            continue
        key = field.name
        value = getattr(self,key)
        if isinstance(value,(date,time,datetime)):  #date,time,datetime   数据类型 不能被 序列化
            value = str(value)                      #转换成 字符串格式
        attr_dict[key] = value
    return attr_dict


def patch_model():
    """通过 Monkey Patch(猴子补丁)的方式 为Django的 ORM 增加统一的缓存"""
    # 修改 get 方法
    QuerySet._get = QuerySet.get
    QuerySet.get = get

    # 修改 save 方法
    models.Model._save = models.Model.save
    models.Model.save = save

    #统一为所有的 Model 增加 to_dict 方法
    models.Model.to_dict = to_dict



