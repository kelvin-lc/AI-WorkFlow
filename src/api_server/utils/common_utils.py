import functools
import logging
import traceback

logger = logging.getLogger(__name__)


def catch_return_default(default=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                logger.warning(str(traceback.format_exc()))
                return default

        return wrapped_func

    return decorator
