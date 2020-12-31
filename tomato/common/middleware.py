from django.utils.deprecation import MiddlewareMixin
from libs.http import render_json
from common import stat
class AuthMiddleware(MiddlewareMixin):
    "登陆检查中间件"
    white_list = ("api/user/get_note","api/user/register","api/user/laoding")

    def process_request(self,request):
        if request.path in self.white_list:
            return

        uid = request.session.get("uid")
        if not uid:
            return render_json(code=stat.LOGIN_REQUIRED)
