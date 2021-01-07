from django.apps import AppConfig
from social.models import swiped
from social.logics import like_someone
from libs.http import render_json

def like_some(request):
    sid = int(request.GET.get("uid"))
    print("sid==",sid)
    is_matched = like_someone("1",sid,"like")
    return render_json()




 