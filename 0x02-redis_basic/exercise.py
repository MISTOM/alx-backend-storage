#!/usr/bin/env python3
'''A module for using Redis; NoSQL Data Storage
'''


from typing import Callable, Union
from functools import wraps
import redis
import uuid


def count_calls(method: Callable) -> Callable:
    '''Tracks the number of calls made to a method in a Cache class.
    '''
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        '''Invokes the given method after incrementing its call counter.
        '''
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return invoker


def call_history(method: Callable) -> Callable:
    '''Tracks the call details of a method in a Cache class.
    '''
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        '''Returns the method's output after storing its inputs and output.
        '''
        in_key = '{}:inputs'.format(method.__qualname__)
        out_key = '{}:outputs'.format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(in_key, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(out_key, output)
        return output
    return invoker


class Cache:
    '''Represents an object for caching data in Redis data storage
    '''
    def __init__(self) -> None:
        '''Initializes Cache instance
        '''
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''Store a value in Redis Data Storage and return the Key
        '''
        rand_key = str(uuid.uuid4())
        self._redis.set(rand_key, data)
        return rand_key

    def get(self, key: str,
            fn: Callable = None
            ) -> Union[str, bytes, int, float]:
        '''Retrieve data from Redis Data Storage
        '''
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        '''Retrieves a string from Redis Data Storage
        '''
        return self.get(key, lambda x: x.decode('utf8'))

    def get_int(self, key: str) -> str:
        '''Retrieves a integer from Redis Data Storage
        '''
        return self.get(key, lambda x: int(x))
