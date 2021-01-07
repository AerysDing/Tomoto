from social.models import swiped
from common import stat
from user.models import user
from user.models import profile
import datetime

def rcmd(uid):
    """用户推荐接口"""
    # 获取当前用户的交友资料
    Profile,_ = profile.objects.get_or_create(id=uid)
    print("--1--",type(Profile),uid)
    # min_dating_age
    #计算出生生日的范围
    today = datetime.date.today()   #今天的日期
    earliest_birthday = today - datetime.timedelta(Profile.max_dating_age * 365)
    lalest_birthday = today - datetime.timedelta(Profile.min_dating_age * 365)
    print("--3--",Profile.dating_location,Profile.dating_location,earliest_birthday,lalest_birthday)
    # 根据条件匹配要推荐的用户
    users = user.objects.filter(
        gender=Profile.dating_gender,
        location=Profile.dating_location,
        birthday__gte=earliest_birthday,
        birthday__lte=lalest_birthday
        )[:30]  #懒加载

    # TODO:排除已经划过的用户
    # 返回最终的结果
    return users



def like_someone(uid,sid,stype):
    # try:
    swipe_test = swiped.objects.create(uid=uid,sid=sid,stype=stype)
    # except swipe_test.IntegrityError:
    #     raise stat.RepeatSwipeErr
