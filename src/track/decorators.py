import os
import sys
from functools import wraps

from icecream import ic as iceicebaby


def handle_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            iceicebaby(e)

            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            iceicebaby(exc_type, fname, exc_tb.tb_lineno)
            return {"failed"}

    return wrapper
