# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import time
from school_api.session import SessionStorage


class MemoryStorage(SessionStorage):
    ''' 非持久化缓存 不推荐使用'''

    def __init__(self, prefix=''):
        self._data = {}
        self.prefix = prefix

    def key_name(self, key):
        return '{0}:{1}'.format(self.prefix, key)

    def get(self, key, default=None):
        key = self.key_name(key)
        value = None
        data = self._data.get(key, default)
        if data:
            if data['expires_at'] is True or data['expires_at'] > time.time():
                # 为True时：永不过期， 大于当前时间为：不到过期时间
                value = data['value']
            else:
                self.delete(key)
        return value

    def set(self, key, value, ttl=None):

        if value is None:
            return

        key = self.key_name(key)
        expires_at = not ttl or time.time() + ttl
        data = {'value': value, 'expires_at': expires_at}
        self._data[key] = data

    def delete(self, key):
        key = self.key_name(key)
        self._data.pop(key, None)