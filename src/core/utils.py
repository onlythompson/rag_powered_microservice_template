import time
from functools import wraps
from .logger import logger

def retry_with_backoff(retries=3, backoff_in_seconds=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            x = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if x == retries:
                        raise
                    else:
                        logger.warning(f"Retrying {func.__name__} due to {str(e)}")
                        time.sleep(backoff_in_seconds * 2 ** x)
                        x += 1
        return wrapper
    return decorator

def sanitize_input(text: str) -> str:
    # Implement input sanitization logic here
    return text.strip()