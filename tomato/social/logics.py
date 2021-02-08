from common import stat
from user.models import user
from user.models import profile
import datetime
from social.models import swiped
from django.db.utils import IntegrityError
from social.models import Friend
from libs.cache import rds
from common import keys
from django.db.models import Q
from tomato.conf import TOMATO_SCORE


def rcmd_from_rds(uid):
     #取出推荐队列里到用户
    uid_list = rds.lrange(keys.FIRST_RCMD % uid,0,29)
    print("--3--",uid_list)
    uid_list = [int(uid) for uid in uid_list]
    return user.objects.filter(id__in=uid_list)


def rcmd_from_db(uid,num):
    # 获取当前用户的交友资料
    Profile,_ = profile.objects.get_or_create(id=uid)
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
        ).exclude(id__in=sid_list)[:30]     #懒加载   #exclude() 排除
    return users


def rcmd(uid):
    """用户推荐接口"""
    filter_suers = rcmd_from_rds(uid)      #首先取出队列中的用户
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
    #为被滑动用户增加积分
    rds.zincrby("HotRank",TOMATO_SCORE["like"],sid)
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
    # 为被滑动用户增加积分
    rds.zincrby("HotRank", TOMATO_SCORE["superlike"], sid)
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
    # 为被滑动用户增加积分
    rds.zincrby("HotRank", TOMATO_SCORE["dislike"], sid)


def rewind_last_swipe(uid):
    """
    反悔上一次的滑动
    每天反悔3次
    反悔记录只能在5分钟内
    """
    #取出当前时间
    now = datetime.datetime.now()
    #检查当前是否反悔了3次
    key = keys.Rewind_K % (now.date(),uid)
    rewind_times = rds.get(key,0) #取出当天的反悔次数
    if rewind_times >= 3:
        #达到：直接给用户提示
        raise stat.RewindLimited
        #未达到：正常进行逻辑处理
    # 找到最后一次的滑动的记录
    latest_swipe = swiped.objects.filter(uid=uid).latest("stime")
    # 距离上一次滑动已经过去的秒数
    passed_time = (now - latest_swipe.stime).total_seconds()
    # 对比当前时间和最后一次的滑动时间
    if passed_time >=300:
       # 否：给用户提示    超过5分钟
       raise stat.RewinTimeout
    if latest_swipe.stype in ["like","superlike"]:
        # 1.好友关系删掉
        Friend.objects.filter(uid1=uid,uid2=latest_swipe.sid).delete()
        if latest_swipe.stype == "superlike":
            # 2.优先推荐列表里的数据删掉
            rds.lrem((keys.FIRST_RCMD % latest_swipe.sid,1,uid))
    rds.zincrby(keys.RANK_K, - TOMATO_SCORE[latest_swipe.stype], latest_swipe.sid)
    # 删除最后一次的滑动记录
    latest_swipe.delete()
    #全部完成后，累加反悔次数
    rds.set(key,rewind_times+1,86400 * 2)





def who_liked_me(uid):
    """找到喜欢过我的人，并且我还有划过对方的人"""
    # 取出所有所有划过的ID
    sid_list = swiped.objects.filter(uid=uid).values_list("sid", flat=True)
    uid_list = swiped.objects.filter(sid=uid,stype__in=["like","superlike"]).exclude(uid__in=sid_list).values_list("uid",flat=True)
    #取出喜欢过自己的用户数据
    users = user.objects.filter(id__in=uid_list)
    return users


def get_my_friends_id(uid):
    """获取用户自己好友ID列表"""
    query_condition = Q(uid1=uid) | Q(uid2=uid)
    friend_list = Friend.objects.filter(query_condition)
    print("---14--",friend_list)
    friend_id = []
    for f in friend_list:
        if f.uid1 == uid:
            friend_id.append(f.uid2)
        else:
            friend_id.append(f.uid1)
    friend = user.objects.filter(id__in=friend_id)
    return friend


def get_top_n(num):
    """获取积分排行最高前50"""

    #取出原始榜单数据
    rank_data = rds.zrevrange(keys.RANK_K,num-1,withscores=True)
    cleaned_rank = [[int(item[0],int(item[1]))] for item in rank_data]        #对原始数据简单处理
    # cleaned_rank = [[int(uid), int(score)] for uid,score in rank_data] 第二种方法
    uid_list = [uid for uid,_ in cleaned_rank]
    User = user.object.filter(id__in = uid_list).only("id","name","avatar")   #顺序已乱
    User = sorted(User,key=lambda user:uid_list.index(user.id))                      #按照列表的索引 从新排序

    #组装数据
    result = {}
    for index ,(uid ,score) in enumerate(cleaned_rank):
        rank = index + 1
        users = User[index]
        users_dict = {
            "id":uid,
            "score":score,
            "nickname":users.nackname,
            "avatar":users.avatar
        }
        result[rank] = users_dict
    return result


"""
Redis
String：普通缓存
Hash：对象到缓存
List：队列或者栈
set：去重，集合运算
Zset：排行榜
"""