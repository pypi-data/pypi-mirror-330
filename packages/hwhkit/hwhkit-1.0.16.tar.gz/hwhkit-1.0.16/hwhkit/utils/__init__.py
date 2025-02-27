# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# Time       ：2024/4/22 18:36
# Author     ：Maxwell
# Description：
"""
import time
from loguru import logger
from typing import List, Callable
from functools import wraps
from inspect import iscoroutinefunction


logger.add("./logs/info.log", level='INFO', rotation="200 MB")
logger.add("./logs/warning.log", level='WARNING', rotation="200 MB")
logger.add("./logs/debug.log", level='DEBUG', rotation="200 MB")
logger.add("./logs/error.log", level='ERROR', rotation="200 MB")


def error_handler(func: Callable):
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            return None

    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            return None

    if iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper


def measure_time(mark="耗时"):
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = await func(*args, **kwargs)
            end_time = time.perf_counter()
            logger.info(f"{mark}: {func.__name__}, {end_time - start_time:.4f} s")
            return result

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            logger.info(f"{mark}: {func.__name__}, {end_time - start_time:.4f} s")
            return result

        if iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    return decorator