from common import stat
from user.models import user

def need_permission(perm_name):
    """检查用户是否具有某种权限"""
    def deco(view_func):
        def wrapper(request,*args,**kwargs):
            #先检查过期时间
            users = user.objects.get(id=request.uid)
            user.check_vip_end_time()
            #在检查是否有权限
            if user.vip.has_perm(perm_name):
                return view_func(request,*args,**kwargs)
            else:
                raise stat.PermRequired
        return wrapper
    return deco