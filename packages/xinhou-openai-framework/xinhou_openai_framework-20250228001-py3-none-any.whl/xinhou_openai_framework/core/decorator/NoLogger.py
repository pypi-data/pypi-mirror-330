from functools import wraps
import inspect

def NoLogger(func):
    """
    禁用日志打印的装饰器，支持同步和异步函数
    """
    if inspect.iscoroutinefunction(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            return await func(*args, **kwargs)
        async_wrapper.no_logger = True
        return async_wrapper
    else:
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        sync_wrapper.no_logger = True
        return sync_wrapper 