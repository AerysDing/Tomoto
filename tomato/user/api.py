from django.shortcuts import render
from django.http import HttpResponse
from user.models import user
from user.models import profile
from libs.cache import rds
from user.logics import send_note
from user.logics import save_avatar
from libs.http import render_json
from common import stat
from common import keys
from user.forms import UserForm
from user.forms import ProfileFrom
import logging

inf_log = logging.getLogger("inf")
from libs.qncloud import upload_to_qn
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
    password = request.POST.get("password")
    vcode =  request.POST.get("vcode")
    key = keys.VCODE_K % phone
    cache_vcode = rds.get(key)
    if vcode and vcode == cache_vcode:
        users = user.objects.create(phone=phone,password=password)

        return render_json()
    else:
        raise stat.VcodeErr


def laoding(request):
    """laoding"""
    phone = request.POST.get("phone")
    password = request.POST.get("password")
    try:
        users = user.objects.get(phone=phone)   #查询集  返回是queryset对象 --懒加载
        inf_log.info(f'User({users.id}:{users.name}) login')
    except users.DoesNotExist:
        raise stat.LogicErr
    if phone == users.phone and password == users.password:
        request.session['uid'] = users.id
        return render_json()
    else:
        raise stat.LogicErr


def get_profile(request):
    uid = str(request.session["uid"])
    key = keys.MODEL_K % (profile.__name__, uid)
    Profile = rds.get(key)
    if Profile == None:
        Profile, _ = profile.objects.get_or_create(id=request.session["uid"])  # get_or_create
        rds.set(key,Profile)
    return render_json(Profile.to_dict())


def modify_profile(request):
    """修改用户信息，及用户配置"""
    user_form = UserForm(request.POST)
    user_profile = ProfileFrom(request.POST)
    if not user_form.is_valid():
        raise stat.UserFormErr(user_form.errors)
    if not user_profile.is_valid():
        raise stat.ProfileFormErr(user_profile.errors)
    # modify user data
    user.object.filter(id=request.uid).update(**user_form.cleaned_data)
    # modify profile data
    profile.object.update_or_create(id=request.uid,defaults=user_profile.cleaned_data)
    # update urllib cache
    key = keys.MODEL_K % (profile.__name__, request.uid)
    rds.delete(key)
    return render_json()


def upload_avater(request):
    """上传形象"""
    # 1.接受用户图片，保存到本地
    avatar_file = request.FILES.get("avatar")
    print(avatar_file)
    save_avatar.delay(request.session["uid"],avatar_file)
    return render_json()
















