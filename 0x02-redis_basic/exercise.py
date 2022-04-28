#!/usr/bin/env python3
'''A module for using Redis; NoSQL Data Storage
'''


from typing import Union
import redis
import uuid


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
