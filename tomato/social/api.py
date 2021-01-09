from libs.http import render_json
from social import logics


def rmcd_user(request):
    "推荐用户"
    users = logics.rcmd(request.session["uid"])
    # print(users)
    result = [user.to_dict() for user in users]
    return render_json(result)


def like(request):
    """右滑:喜欢"""
    sid = request.POST.get("sid")
    print("---5--",sid,request.session["uid"])
    is_matched = logics.like_someone(request.session["uid"],sid)
    return render_json({"is_matched":is_matched})


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
 