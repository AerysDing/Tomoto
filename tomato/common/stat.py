OK = 0
class LogicErr(Exception):
    code = None
    data = None

    def __init__(self,data=None):
        self.data =data or self.__class__.__name__


def gen_logic_err(name,code):   #创建类

    return type(name,(LogicErr,),{"code":code})       #type 元类   创建类

#工厂模式
#type(name,bases,dict)   name 类名  bases 继承的类  dict属性字典

SmsErr = gen_logic_err("SmsErr",1000)                   #短信发送失败
VcodeErr = gen_logic_err("vcodeErr",1001)               #短信验证失败
LoginRequired = gen_logic_err("LoginRequired",1002)     #短信验证失败
UserFormErr = gen_logic_err('UserFormErr', 1003)        #用户表单数据错误
ProfileFormErr = gen_logic_err('ProfileFormErr', 1004)  #用户资料表单错误
RepeatSwipeErr = gen_logic_err('RepeatSwipeErr', 1005)  #重复滑动的错误
LOGIN_REQUIRED = gen_logic_err("LOGIN_REQUIRE",1006)
AreadyFriends = gen_logic_err('AreadyFriends', 1007)    # 两者已经是好友，无需重复添加
RewindLimited = gen_logic_err("RewindLimited",1008)     #反悔次数已经达到上线
RewindTimeout_K = gen_logic_err("RewindTimeout",1009)   #超出反悔时间
PermRequired =  gen_logic_err("PermRequired",1010)      #缺少某种权限