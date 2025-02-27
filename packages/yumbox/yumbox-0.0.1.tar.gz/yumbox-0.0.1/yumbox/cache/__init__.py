import functools
import os
import pickle
from time import sleep
from typing import Callable, Optional

import faiss
import numpy as np

from yumbox.config import BFG

# TODO: To prevent corruption on power outage,
# save to temp location then move to target.


def cache(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        cache_dir = BFG["cache_dir"]
        logger = BFG["logger"]

        func_name = func.__name__
        cache_file = ""
        if cache_dir:
            cache_file = os.path.join(cache_dir, func_name)
            cache_file += ".pkl"

        if cache_dir and os.path.isfile(cache_file):
            logger.info(f"Loading cache for {func_name} from {cache_dir}")
            with open(cache_file, "rb") as fd:
                return pickle.load(fd)
        else:
            result = func(*args, **kwargs)
            if cache_dir:
                logger.info(f"Saving cache for {func_name} to {cache_dir}")
                with open(cache_file, "wb") as fd:
                    pickle.dump(result, fd)
                logger.info(f"Saved cache!")
            return result

    return wrapper


def cache_wargs(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        cache_dir = BFG["cache_dir"]
        logger = BFG["logger"]

        func_name = func.__name__
        func_kwargs = []
        for k, v in kwargs.items():
            func_kwargs.append(f"{k}-{v}")
        func_kwargs = " ".join(func_kwargs)
        cache_file = ""
        if cache_dir:
            cache_file = os.path.join(cache_dir, func_name + func_kwargs)
            cache_file += ".pkl"

        if cache_dir and os.path.isfile(cache_file):
            logger.info(f"Loading cache for {func_name} from {cache_dir}")
            with open(cache_file, "rb") as fd:
                return pickle.load(fd)
        else:
            result = func(*args, **kwargs)
            if cache_dir:
                logger.info(f"Saving cache for {func_name} to {cache_dir}")
                with open(cache_file, "wb") as fd:
                    pickle.dump(result, fd)
                logger.info(f"Saved cache!")
            return result

    return wrapper


def async_cache(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        cache_dir = BFG["cache_dir"]
        logger = BFG["logger"]

        func_name = func.__name__
        cache_file = ""
        if cache_dir:
            cache_file = os.path.join(cache_dir, func_name)
            cache_file += ".pkl"

        if cache_dir and os.path.isfile(cache_file):
            logger.info(f"Loading cache for {func_name} from {cache_dir}")
            with open(cache_file, "rb") as fd:
                return pickle.load(fd)
        else:
            result = await func(*args, **kwargs)
            if cache_dir:
                logger.info(f"Saving cache for {func_name} to {cache_dir}")
                with open(cache_file, "wb") as fd:
                    pickle.dump(result, fd)
                logger.info(f"Saved cache!")
            return result

    return wrapper


def index(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        cache_dir = BFG["cache_dir"]
        logger = BFG["logger"]

        func_name = func.__name__
        cache_file = ""
        if cache_dir:
            cache_file = os.path.join(cache_dir, func_name)
            cache_file += ".bin"

        if cache_dir and os.path.isfile(cache_file):
            logger.info(f"Loading cache for {func_name} from {cache_dir}")
            return faiss.read_index(cache_file)
        else:
            result = func(*args, **kwargs)
            if cache_dir:
                logger.info(f"Saving cache for {func_name} to {cache_dir}")
                faiss.write_index(result, cache_file)
                logger.info(f"Saved cache!")
            return result

    return wrapper


def np_cache(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        cache_dir = BFG["cache_dir"]
        logger = BFG["logger"]

        func_name = func.__name__
        cache_file = ""
        if cache_dir:
            cache_file = os.path.join(cache_dir, func_name)
            cache_file += ".npz"

        if cache_dir and os.path.isfile(cache_file):
            logger.info(f"Loading cache for {func_name} from {cache_dir}")
            res = np.load(cache_file)
        else:
            res = None
        res = func(*args, **kwargs, cache=res, cache_file=cache_file)
        if cache_dir:
            logger.info(f"Saving cache for {func_name} to {cache_dir}")
            np.savez(cache_file, keys=list(res.keys()), values=list(res.values()))
            logger.info(f"Saved cache!")
        return res

    return wrapper


def kv_cache(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        cache_dir = BFG["cache_dir"]
        logger = BFG["logger"]

        func_name = func.__name__
        cache_file = ""
        if cache_dir:
            cache_file = os.path.join(cache_dir, func_name)
            cache_file += ".pkl"

        if cache_dir and os.path.isfile(cache_file):
            logger.info(f"Loading cache for {func_name} from {cache_dir}")
            with open(cache_file, "rb") as fd:
                res = pickle.load(fd)
        else:
            res = None
        res = func(*args, **kwargs, cache=res, cache_file=cache_file)
        if cache_dir:
            logger.info(f"Saving cache for {func_name} to {cache_dir}")
            with open(cache_file, "wb") as fd:
                pickle.dump(res, fd)
            logger.info(f"Saved cache!")
        return res

    return wrapper


def coalesce(*args):
    # Return the first non-None value
    return next((x for x in args if x is not None))


def retry(max_tries=5, wait=3, validator: Optional[Callable] = None):
    """Args max_tries and wait defined as class attributes have higher precedence."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0] if len(args) else None
            tries = coalesce(getattr(self, "max_tries", None), max_tries)
            delay = coalesce(getattr(self, "wait", None), wait)
            success = False
            for retry in range(0, tries):
                try:
                    response = func(*args, **kwargs)
                    if validator:
                        validator(*args, **kwargs, response=response)
                    success = True
                except Exception as e:
                    if retry + 1 < tries:
                        print(f"Exception {e} occured, retrying {retry+1}/{tries}")
                        sleep(delay)
                    continue
            if success == True:
                return response
            else:
                return {"status": "error", "error": {"message": str(e)}}

        return wrapper

    return decorator


def last_offset(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        cache_dir = BFG["cache_dir"]
        logger = BFG["logger"]

        func_name = func.__name__ + "_" + last_offset.__name__
        cache_file = ""
        if cache_dir:
            cache_file = os.path.join(cache_dir, func_name)
            cache_file += ".txt"

        if cache_dir and os.path.isfile(cache_file):
            logger.info(f"Loading cache for {func_name} from {cache_dir}")
            with open(cache_file, "r") as fd:
                offset = fd.readline().strip()
        else:
            offset = None

        result = func(*args, **kwargs, offset=offset)
        offset = result["offset"]
        if cache_dir:
            logger.info(f"Saving cache for {func_name} to {cache_dir}")
            with open(cache_file, "w") as fd:
                fd.write(offset)
            logger.info(f"Saved cache!")
        return result

    return wrapper
