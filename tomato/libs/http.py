import json
from django.http import HttpResponse
from django.conf import settings
from common import stat

def render_json(data=None, code=stat.OK):
    result = {
        "data":data,
        "code":code
    }
    if settings.DEBUG:
        json_data = json.dumps(result,ensure_ascii=False,indent=4,sort_keys=True)
    else:
        json_data = json.dumps(result,ensure_ascii=False,separators=(",",":"))
    return HttpResponse(json_data)

