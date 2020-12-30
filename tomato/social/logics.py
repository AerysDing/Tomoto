from social.models import swiped
from common import stat


def like_someone(uid,sid,stype):
    # try:
    swipe_test = swiped.objects.create(uid=uid,sid=sid,stype=stype)
    # except swipe_test.IntegrityError:
    #     raise stat.RepeatSwipeErr
