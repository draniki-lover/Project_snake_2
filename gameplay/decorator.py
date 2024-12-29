from functools import wraps

def log_action(action_name):
    """
    Декоратор для логирования действий
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator