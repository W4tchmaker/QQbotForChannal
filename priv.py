"""The privilege of user discribed in an `int` number.

`0` is for Default or NotSet. The other numbers may change in future versions.
"""

from datetime import datetime
import config

BLACK = -999
DEFAULT = 0
NORMAL = 1
PRIVATE = 10
ADMIN = 21
OWNER = 22
WHITE = 51
SUPERUSER = 999
SU = SUPERUSER

#===================== block list =======================#
_black_channel = {}  # Dict[channel_id, expr_time]
_black_user = {}  # Dict[user_id, expr_time]


def set_block_channel(channel_id, time):
    _black_channel[channel_id] = datetime.now() + time


def set_block_user(user_id, time):
    if user_id not in config.SUPERUSERS:
        _black_user[user_id] = datetime.now() + time


def check_block_channel(channel_id):
    if channel_id in _black_channel and datetime.now() > _black_channel[channel_id]:
        del _black_channel[channel_id]  # 拉黑时间过期
        return False
    return bool(channel_id in _black_channel)


def check_block_user(user_id):
    if user_id in config.BLACK_LIST:
        return True
    if user_id in _black_user and datetime.now() > _black_user[user_id]:
        del _black_user[user_id]  # 拉黑时间过期
        return False
    return bool(user_id in _black_user)


#========================================================#


def get_user_priv(message):
    uid = message.author
    if uid in config.SUPERUSERS:
        return SUPERUSER
    if check_block_user(uid):
        return BLACK
    if uid in config.WHITE_LIST:
        return WHITE
    else:
        return NORMAL
