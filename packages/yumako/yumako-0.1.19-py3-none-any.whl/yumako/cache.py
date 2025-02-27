import json
import logging
import os
from datetime import datetime
from typing import Any, Callable, TypeVar, cast

logger = logging.getLogger(__name__)

T = TypeVar("T")


def _with_cache_impl(fn_populate_data: Callable[[], T], file_name: str, ttl_seconds: int) -> T:
    """Implementation of the file caching mechanism.

    Args:
        fn_populate_data: Function that generates the data to be cached
        file_name: Path to the cache file
        ttl_seconds: Time-to-live in seconds for the cache

    Returns:
        The cached data or newly generated data
    """
    try:
        if os.path.exists(file_name):
            file_modified = datetime.fromtimestamp(os.path.getmtime(file_name))
            delta_seconds = (datetime.now() - file_modified).total_seconds()
            if delta_seconds <= ttl_seconds:
                logger.info(f"Using cache: {file_name}")
                with open(file_name) as f:
                    return cast(T, json.load(f))

        logger.info(f"Populating data: {file_name}")
        data = fn_populate_data()
        if data is not None:
            logger.info(f"Writing cache: {file_name}")
            os.makedirs(os.path.dirname(file_name), exist_ok=True)
            with open(file_name, "w") as f:
                json.dump(data, f, indent=4)
        else:
            logger.info(f"Empty data: {file_name}")
        return data
    except Exception as e:
        logger.error(f"Cache error for {file_name}: {str(e)}")
        return fn_populate_data()


def file_cache(file_name: str, ttl_seconds: int = 24 * 60 * 60) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator that caches function results in a JSON file.

    Args:
        file_name: Path to the cache file
        ttl_seconds: Time-to-live in seconds for the cache (default: 24 hours)

    Returns:
        A decorator function that implements the caching behavior

    Example:
        @file_cache('data.json', ttl_seconds=3600)
        def fetch_data():
            return {'key': 'value'}
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        def wrapper(*args: Any, **kwargs: Any) -> T:
            def populate_data() -> T:
                return func(*args, **kwargs)

            return _with_cache_impl(populate_data, file_name, ttl_seconds)

        return wrapper

    return decorator
