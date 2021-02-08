from redis import Redis as _redis
from tomato.conf import REDIS
import pickle

class Redis(_redis):

    def set(self, name, value,ex=None, px=None, nx=False, xx=False, keepttl=False):
        pickle_value = pickle.dumps(value,pickle.HIGHEST_PROTOCOL)
        return super().set(name,pickle_value,ex,px,nx,xx)

    def get(self, name, default=None):
        '''Return the value at key ``name``, or ``default`` if the key doesn't exist'''
        pickled_value = super().get(name)
        if pickled_value is None:
            return default
        else:
            try:
                value = pickle.loads(pickled_value)
            except pickle.UnpicklingError:
                return pickled_value
            else:
                return value

rds =Redis(**REDIS)


