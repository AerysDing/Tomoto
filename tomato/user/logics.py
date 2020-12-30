import random
from common import keys
from tomato import conf
import requests
from libs.cache import rds
from uuid import uuid4
from libs.qncloud import upload_to_qn
import os


def code(length=6):
    char = []
    for i in range(length):
        char.append(str(random.randint(0,9)))
    return "".join(char)


def send_note(mobile):
    key = keys.VCODE_K % mobile
    if rds.get(key):
        return
    vcode = code()
    arg = conf.YZX_SMS_ARGS.copy()
    arg["param"] = vcode
    arg["mobile"] = mobile
    reponse = requests.post(conf.YZX_SMS_API,json=arg)
    # result = reponse.json()
    # print(result)
    print(reponse.status_code)
    if reponse.status_code == 200:
        result = reponse.json()
        print(result.get("code"))
        if result.get("code") == "000000":
            rds.set(key,vcode,600)
            print("rds========>")
            return True
        else:
            return False
    return False


def save_tmp_file(tmp_file):
    '''save temporary files'''
    tmp_filename = uuid4().hex
    tmp_filepath = '/tmp/%s' % tmp_filename
    with open(tmp_filepath, 'wb') as fp:
        for chunk in tmp_file.chunks():      # Don't understand , what is tmp_file.chunks() funation
            fp.write(chunk)
    return tmp_filepath, tmp_filename


def save_avatar(avatar_file):
    '''保存用户形象图片'''
    filepath, filename = save_tmp_file(avatar_file)
    print(filename,filepath)
    # 2. 上传到七牛云
    url = upload_to_qn(filepath, filename)
    # 3. 更新用户的 avatar 字段
    # user.objects.filter(id=uid).update(avatar=url)
    # 4. 删除本地的临时文件
    os.remove(filepath)
    return url


