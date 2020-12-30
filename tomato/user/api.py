from django.shortcuts import render
from django.http import HttpResponse
from user.models import user
from user.models import profile
from libs.cache import rds
from user.logics import send_note
from user.logics import save_tmp_file
from libs.http import render_json
from common import stat
from common import keys
from user.forms import UserForm
from user.forms import ProfileFrom
from user.logics import save_avatar
# Create your views here.


def get_note(request):
    """get note"""
    phone = request.GET.get("phone")
    vcode = send_note(phone)
    if vcode:
        return render_json()
    else:
        raise stat.SmsErr


def register(request):
    "register"
    phone = request.POST.get("phone")
    print("request-POST",request.POST)
    password = request.POST.get("password")
    vcode =  request.POST.get("vcode")
    key = keys.VCODE_K % phone
    cache_vcode = rds.get(key)
    print("vcode",cache_vcode)
    if vcode and vcode == cache_vcode:
        users = user.objects.create(phone=phone,password=password)
        return render_json()
    else:
        raise stat.VcodeErr


def laoding(request):
    """laoding"""
    phone = request.POST.get("phone")
    password = request.POST.get("password")
    print("loading",phone,password)
    try:
        users = user.objects.get(phone=phone)   #查询集  返回是queryset对象 --懒加载
    except users.DoesNotExist:
        raise stat.LogicErr
    if phone == users.phone and password == users.password:
        request.session['uid'] = users.id
        return render_json()
    else:
        raise stat.LogicErr


def get_profile(request):
    print("uid==",request.uid)
    key = keys.MODEL_K(profile.__name__,request.uid)
    Profile = rds.get(key)
    if Profile == None:
        Profile, _ = profile.objects.get_or_create(id=request.uid)  # get_or_create
        rds.set(key,Profile)
    return render_json()


def modify_profile(request):
    """修改用户信息，及用户配置"""
    user_form = UserForm(request.POST)
    user_profile = ProfileFrom(request.POST)
    if not user_form.is_valid():
        raise stat.UserFormErr(user_form.errors)
    if not user_profile.is_valid():
        raise stat.ProfileFormErr(user_profile.errors)
    # 修改用户数据
    user.object.filter(id=request.uid).update(**user_form.cleaned_data)
    # 修改profile数据
    profile.object.update_or_create(id=request.uid,defaults=user_profile.cleaned_data)
    # 更新urllib缓存
    key = keys.MODEL_K % (profile.__name__, request.uid)
    rds.delete(key)
    return render_json()


def upload_avater(request):
    avter_file = request.FILES.get("avatar")
    a = save_avatar(avter_file)
    print(a)
    return render_json()













