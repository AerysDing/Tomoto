from common import stat
from user.models import user
from user.models import profile
import datetime
from social.models import swiped
from django.db.utils import IntegrityError
from social.models import Friend
from libs.cache import rds
from common import keys

def rcmd_from_rds(uid):
     #取出推荐队列里到用户
    uid_list = rds.lrange(keys.FIRST_RCMD % uid,0,29)
    print("--3--",uid_list)
    uid_list = [int(uid) for uid in uid_list]
    return user.objects.filter(id__in=uid_list)


def rcmd_from_db(uid,num):
    # 获取当前用户的交友资料
    Profile,_ = profile.objects.get_or_create(id=uid)
    print("--1--",type(Profile),uid)
    # min_dating_age
    #计算出生生日的范围
    today = datetime.date.today()   #今天的日期
    earliest_birthday = today - datetime.timedelta(Profile.max_dating_age * 365)
    lalest_birthday = today - datetime.timedelta(Profile.min_dating_age * 365)
    print("--3--",Profile.dating_location,Profile.dating_location,earliest_birthday,lalest_birthday)
    # TODO:排除已经划过的用户
    # 取出所有所有划过的ID
    sid_list = swiped.objects.filter(uid=uid).values_list("sid", flat=True)

    # 根据条件匹配要推荐的用户
    users = user.objects.filter(
        gender=Profile.dating_gender,
        location=Profile.dating_location,
        birthday__gte=earliest_birthday,
        birthday__lte=lalest_birthday
        ).exclude(id__in=sid_list)[:30]  #懒加载   #exclude() 排除
    return users


def rcmd(uid):
    """用户推荐接口"""
    filter_suers = rcmd_from_rds(uid) #首先取出队列中的用户
    print("--5---",filter_suers)
    num = len(filter_suers)
    if num >= 30: #如果数量满足30个直接返回
        return filter_suers
    else:
        #不满足从DB 中补齐
        other_users = rcmd_from_db(uid,30-num)
        users = filter_suers | other_users  #将两部分的结果拼在一起
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


def superlike_some(uid,sid):
    """上滑 超级喜欢"""
    # 添加一条滑动记录（不允许重复滑动某人）
    try:
        swiped.objects.create(uid=uid, sid=sid, stype="superlike")  # 联合唯一报错
    except IntegrityError:  # 捕获错误
        raise stat.RepeatSwipeErr
    # 强制从自己优先队列删除 sid
    rds.lrem(keys.FIRST_RCMD % uid, 1, sid)
    # 检查对方的是否划过我  检查是否可以匹配成好友
    result = swiped.objects.filter(uid=sid, sid=uid, stype__in=["like", "superlike"]).exists()
    if result:
        try:
            Friend.objects.create(uid1=sid, uid2=uid)
            return True
        except IntegrityError:
            raise stat.AreadyFriends
    else:
    #将自己的UID 添加到对方推荐队列
        rds.rpush(keys.FIRST_RCMD % sid, uid)
        return False


def dislike_someone(uid,sid):
    """左滑（不喜欢某人）某人"""
    # 添加一条滑动记录（不允许重复滑动某人）
    try:
        swiped.objects.create(uid=uid, sid=sid, stype="dislike")  # 联合唯一报错
    except IntegrityError:  # 捕获错误
        raise stat.RepeatSwipeErr
    rds.lrem(keys.FIRST_RCMD %  uid, 1, sid)



"""
Redis
String：普通缓存
Hash：对象到缓存
List：队列或者栈
set：去重，集合运算
Zset：排行榜
"""