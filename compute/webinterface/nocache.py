from functools import update_wrapper, wraps
from datetime import datetime
from flask import make_response


# Module for disabling cache in browsers (workaround for issues where changes aren't updated unless cache is cleared)
# Will probably not be relevant for the final ... prototype.
def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response

    return update_wrapper(no_cache, view)
