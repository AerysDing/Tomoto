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
        else:
            request.uid = uid   # 动态增加 uid 属性


#Session 处理过程
# class SessionMiddleware(MiddlewareMixin):
#     def __init__(self, get_response=None):
#         self.get_response = get_response
#         engine = import_module(settings.SESSION_ENGINE)  储存方式数据库
#         self.SessionStore = engine.SessionStore      创建实例
#
#     def process_request(self, request):
#         session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
#         request.session = self.SessionStore(session_key)   从数据库中找session_key  没有返回None   有建立会话机制
#
#     def process_response(self, request, response):
#         """
#         If request.session was modified, or if the configuration is to save the
#         session every time, save the changes and set a session cookie or delete
#         the session cookie if the session has been emptied.
#         """
#         try:
#             accessed = request.session.accessed
#             modified = request.session.modified
#             empty = request.session.is_empty()
#         except AttributeError:
#             pass
#         else:
#             # First check if we need to delete this cookie.
#             # The session should be deleted only if the session is entirely empty
#             if settings.SESSION_COOKIE_NAME in request.COOKIES and empty:
#                 response.delete_cookie(
#                     settings.SESSION_COOKIE_NAME,
#                     path=settings.SESSION_COOKIE_PATH,
#                     domain=settings.SESSION_COOKIE_DOMAIN,
#                 )
#             else:
#                 if accessed:
#                     patch_vary_headers(response, ('Cookie',))
#                 if (modified or settings.SESSION_SAVE_EVERY_REQUEST) and not empty:
#                     if request.session.get_expire_at_browser_close():
#                         max_age = None
#                         expires = None
#                     else:
#                         max_age = request.session.get_expiry_age()
#                         expires_time = time.time() + max_age
#                         expires = cookie_date(expires_time)
#                     # Save the session data and refresh the client cookie.
#                     # Skip session save for 500 responses, refs #3881.
#                     if response.status_code != 500:
#                         try:
#                             request.session.save()                        session保存到数据库   bash64 加密 并制作一个key
#                         except UpdateError:
#                             raise SuspiciousOperation(
#                                 "The request's session was deleted before the "
#                                 "request completed. The user may have logged "
#                                 "out in a concurrent request, for example."
#                             )
#                         response.set_cookie(                                             # response.set_cookie    把 session key 传给cookie
#                             settings.SESSION_COOKIE_NAME,
#                             request.session.session_key, max_age=max_age,
#                             expires=expires, domain=settings.SESSION_COOKIE_DOMAIN,
#                             path=settings.SESSION_COOKIE_PATH,
#                             secure=settings.SESSION_COOKIE_SECURE or None,
#                             httponly=settings.SESSION_COOKIE_HTTPONLY or None,
#                         )
#         return response

class LogicErrMiddleware(MiddlewareMixin):
    def process_exception(self,request,exception):               #  as e 传参(exception)  e 和 exception 是一个异常的实例
        if isinstance(exception,stat.LogicErr):              #  exception 是logiceErr 的实例
            return render_json(exception.data,exception.code)

