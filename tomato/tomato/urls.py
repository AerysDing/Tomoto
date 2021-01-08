"""tomato URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url

from user import api as user_api
from social import api as social_api
urlpatterns = [
  #用户模块接口
  url(r'^api/user/get_note',user_api.get_note),
  url(r'^api/user/register',user_api.register),
  url(r'^api/user/laoding',user_api.laoding),
  url(r'^api/user/get_profile',user_api.get_profile),
  url(r'^api/user/modify_profile',user_api.modify_profile),
  url(r'^api/user/upload_avater',user_api.upload_avater),
  #社交模块的接口
  url(r'^api/social/rmcd_user',social_api.rmcd_user),
  url(r'^api/social/like',social_api.like),

]
