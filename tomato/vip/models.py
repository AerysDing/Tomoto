from django.db import models

# Create your models here.
class Vip(models.Model):
    """会员表"""
    name = models.CharField(max_length=16,verbose_name="会员名称")
    level = models.IntegerField(default=0,verbose_name="会员等级")
    duration = models.IntegerField(default=0,verbose_name="购买时常")
    price = models.FloatField(default=0,verbose_name="会员价格")

class Permission(models.Model):
    """"权限的表"""
    name = models.CharField(max_length=16,verbose_name="权限名称")
    description = models.TextField(verbose_name="权限秒数")

class VipPermRelation(models.Model):
    vip_level =models.IntegerField(verbose_name="会员等级")
    perm_id = models.IntegerField(verbose_name="权限ID")
