OK = 0
class LogicErr(Exception):
    code = None
    data = None

    def __init__(self,data=None):
        self.data =data or self.__class__.__name__


def gen_logic_err(name,code):

    return type(name,(LogicErr,),{"code":code})


SmsErr = gen_logic_err("SmsErr",1000)      #短信发送失败
VcodeErr = gen_logic_err("vcodeErr",1001)  #短信验证失败
LoginRequired = gen_logic_err("LoginRequired",1002)     #短信验证失败
UserFormErr = gen_logic_err('UserFormErr', 1003)        # 用户表单数据错误
ProfileFormErr = gen_logic_err('ProfileFormErr', 1004)  # 用户资料表单错误
RepeatSwipeErr = gen_logic_err('RepeatSwipeErr', 1005)  # 重复滑动的错误
LOGIN_REQUIRED = gen_logic_err("LOGIN_REQUIRE",1006)