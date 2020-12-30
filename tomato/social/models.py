from django.db import models

# Create your models here.
class swiped(models.Model):
    """滑动几率"""
    STYPE = (
        ("like","右滑"),
        ("superlike","上滑"),
        ("dislike","左滑"),
    )
    uid = models.ImageField(verbose_name="用户 ID")
    sid = models.ImageField(verbose_name="被滑动用户的ID")
    stype = models.CharField(max_length=10)
    stime = models.DateTimeField(auto_created=True,verbose_name="滑动时间")
    class Meta:
        unique_together = ("uid","sid")


