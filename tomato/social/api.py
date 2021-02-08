from libs.http import render_json
from social import logics
from vip.logics import need_permission

def rmcd_user(request):
    """推荐用户"""
    users = logics.rcmd(request.session["uid"])
    # print(users)
    result = [user.to_dict() for user in users]
    return render_json(result)


def like(request):
    """右滑:喜欢"""
    sid = request.POST.get("sid")
    is_matched = logics.like_someone(request.session["uid"],sid)
    return render_json({"is_matched":is_matched})


@need_permission("superlike")
def superlike(request):
    """上滑：超级喜欢"""
    sid = request.POST.get("sid")
    is_matched = logics.superlike_some(request.session["uid"], sid)
    return render_json({"is_matched": is_matched})


def dislike(request):
    """左滑：不喜欢"""
    sid = request.POST.get("sid")
    print("---7---",request.uid,sid)
    logics.dislike_someone(request.uid,sid)
    return render_json()


def rewind(request):
    """反悔接口"""
    logics.rewind_last_swipe(request.uid)
    return render_json()


def show_who_like_me(request):
    """查看都有谁喜欢过我"""
    print("----8----",request.uid)
    users = logics.who_liked_me(request.uid)
    result =  [user.to_dict() for user in users]
    return render_json(result)


def friends(request):
    """获取朋友列表"""
    friends_list = logics.get_my_friends_id(request.uid)
    result = [user.to_dict() for user in friends_list]
    return render_json(result)



def hot_rank(request):
    """全服人气热度排行榜"""
    rank_data = logics.get_top_n(50)
    return render_json(rank_data)


