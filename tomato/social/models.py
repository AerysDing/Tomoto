from django.db import models

# Create your models here.


class swiped(models.Model):
    """滑动记录"""
    STYPE = (
        ("like","右滑"),
        ("superlike","上滑"),
        ("dislike","左滑"),
    )
    uid = models.IntegerField(verbose_name="用户 ID")
    sid = models.IntegerField(verbose_name="被滑动用户的ID")
    stype = models.CharField(max_length=10,choices=STYPE,verbose_name="滑动类型")
    stime = models.DateTimeField(auto_now_add=True,verbose_name="滑动时间")
    class Meta:
        unique_together = ("uid","sid")   # 联合唯一


class Friend(models.Model):
    """好友表"""
    uid1 = models.IntegerField(verbose_name="用户ID")
    uid2 = models.IntegerField(verbose_name="用户ID")

    class Meta:
        unique_together = ("uid1", "uid2")


