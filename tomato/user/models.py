from django.db import models

# Create your models here.
from django.db import models

class user(models.Model):
    """user表的数据类型"""
    GENDERS =(
        ("male","男性"),
        ("female","女性")
    )

    LOCATION = (
        ("北京","北京"),
        ("上海","上海"),
        ("深圳","深圳"),
        ("苏州","苏州"),
        ("西安","西安"),
        ("武汉","武汉"),
        ("沈阳","武汉"),
    )
    name = models.CharField(max_length=20,verbose_name="昵称")
    phone = models.CharField(max_length=20,verbose_name="手机号")
    gender = models.CharField(max_length=10,default="male",choices=GENDERS,verbose_name="性别")
    birthday = models.DateField(default="1990-01-01",verbose_name="生日")
    location = models.CharField(max_length=20,default="北京",choices=LOCATION,verbose_name="常居地")
    avatar = models.CharField(max_length=256,verbose_name="个人形象的URL")
    password = models.CharField(max_length=254,default="123",verbose_name="密码")
    class Meta:
        db_table = "user"


class profile(models.Model):
    """profile表的数据类型"""
    dating_gender = models.CharField(max_length=10,default="female",choices=user.GENDERS,verbose_name="匹配的性别")
    dating_location = models.CharField(max_length=20,default="北京",choices=user.LOCATION,verbose_name="匹配位置")
    min_distance = models.IntegerField(default=1,verbose_name="最新查找范围")
    max_distance = models.IntegerField(default=10,verbose_name="最大查找范围")
    min_dating_age = models.IntegerField(default=18,verbose_name="最小交友年纪")
    max_dating_age = models.IntegerField(default=60,verbose_name="最大交友年纪")
    vibration = models.BooleanField(default=True, verbose_name='是否开启震动')
    only_matched = models.BooleanField(default=True, verbose_name='不让未匹配的人看我的相册')
    auto_play = models.BooleanField(default=True, verbose_name='自动播放视频')
    class Meta:
        db_table = "profile"






