from common import stat
from user.models import user
from user.models import profile
import datetime
from social.models import swiped
from django.db.utils import IntegrityError
from social.models import Friend

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



def like_someone(uid,sid):
    """右滑：喜欢某人"""
    #添加一条滑动记录（不允许重复滑动某人）
    try:
        swiped.objects.create(uid=uid,sid=sid,stype="like") #联合唯一报错
    except IntegrityError:  #捕获错误
        raise  stat.RepeatSwipeErr
    #检查对方的是否划过我  检查是否可以匹配成好友
    result = swiped.objects.filter(uid=sid,sid=uid,stype__in = ["like","superlike"]).exists()
    if result:
        try:
            Friend.objects.create(uid1=sid,uid2=uid)
            return True
        except:
            raise stat.AreadyFriends
    else:
        return False


