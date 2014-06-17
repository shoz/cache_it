# -*- coding: utf-8 -*-

__all__ = ['init_cache', 'cache_it']

import pylibmc
import functools
import inspect

cache = None

def init_cache(hosts=['127.0.0.1:11211']):
    global cache
    cache = _make_cache(hosts)
    if cache == None:
        raise Exception("Can't connect cache servers. %s" % hosts)

def _make_cache(servers):
    return pylibmc.Client(servers,
                          binary=True,
                          behaviors={'tcp_nodelay':True,
                                     'ketama': True})

def cache_it(*args1, **kwargs1):
    def wrapper1(func):
        @functools.wraps(func)
        def wrapper2(*args2, **kwargs2):
            prefix = kwargs1.get('prefix', None)
            if type(prefix) == unicode:
                prefix = prefix.encode('utf-8')
            ttl = kwargs1.get('ttl', 24 * 60 * 60)
            decoder = kwargs1.get('decoder', lambda x: x)
            encoder = kwargs1.get('encoder', lambda x: x)
            ignore_exception = kwargs1.get('ignore_exception', False)
            debug = kwargs1.get('debug', False)
            if not prefix:
                if inspect.isclass(type(args2[0])):
                    if hasattr(args2[0].__class__, 'CACHE_PREFIX'):
                        prefix = args2[0].__class__.CACHE_PREFIX
                    else:
                        raise ValueError('You must set "prefix" parameter or "CACHE_PREFIX" attribute to cache it.')
            for e in args2:
                if (type(e) == str
                    or type(e) == unicode
                    or type(e) == int):
                    key = e
                    break
            if type(key) == int:
                key = str(key)
            elif type(key) == str:
                key = key
            elif type(key) == unicode:
                key = key.encode('utf-8')
            key = (prefix + key)[:250].rstrip()
            if not _is_ascii(key):
                key = key.encode('base64')
            try:
                cached_data = cache.get(key)
            except Exception as e:
                if not ignore_exception:
                    raise e
                cached_data = None
            if cached_data:
                result = decoder(cached_data)
                if debug:
                    return {
                        'result': result,
                        'is_cache': True
                    }
                else:
                    return result
            else:
                data = func(*args2, **kwargs2)
                try:
                    cache.set(key, encoder(data), time=ttl)
                except Exception as e:
                    if not ignore_exception:
                        raise e
                if debug:
                    return {
                        'result': data,
                        'is_cache': False
                    }
                else:
                    return data
        return wrapper2
    return wrapper1

def _is_ascii(s):
    return all(ord(c) < 128 for c in s)
