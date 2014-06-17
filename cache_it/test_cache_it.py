# -*- coding: utf-8 -*-

from nose.tools import raises
from cache_it import cache_it, init_cache, cache
import switchcache

class CacheConfig:
    HOSTS = ['127.0.0.1:11211']
switchcache.init(CacheConfig)

def setup():
    init_cache()

@switchcache.twice
def _test_normal():
    @cache_it(prefix='test:', debug=True)
    def get_item(key):
        value = key + 'value'
        return value
    ret = get_item('test')
    assert ret['result'] == 'testvalue'
    return ret

@switchcache.twice
def _test_unicode_prefix():
    @cache_it(prefix=u'test:', debug=True)
    def get_item(key):
        value = key + 'value'
        return value
    ret = get_item('test')
    assert ret['result'] == 'testvalue'
    return ret

@switchcache.twice
def _test_unicode_key():
    @cache_it(prefix='test:', debug=True)
    def get_item(key):
        value = key + 'value'
        return value
    ret = get_item(u'test')
    assert ret['result'] == 'testvalue'
    return ret

@switchcache.twice
def _test_multibyte_prefix():
    @cache_it(prefix=u'てすと:', debug=True)
    def get_item(key):
        value = key + 'value'
        return value
    ret = get_item('test')
    assert ret['result'] == 'testvalue'
    return ret

@switchcache.twice
def _test_multibyte_key():
    @cache_it(prefix='test:', debug=True)
    def get_item(key):
        value = key
        return value
    ret = get_item(u'てすと')
    assert ret['result'] == u'てすと'
    return ret

@switchcache.twice
def _test_with_json_coder():
    @cache_it(prefix='test:',
              encoder=lambda x: x['hoge'],
              decoder=lambda x: {'hoge': x},
              debug=True)
    def get_item(key):
        value = {'hoge': 'fuga'}
        return value
    ret = get_item('hoge')
    assert ret['result'] == {'hoge': 'fuga'}
    return ret

@switchcache.twice
def _test_class():
    class Test:
        @cache_it(prefix='test:', debug=True)
        def get_item(self, key):
            return 'value'
    c = Test()
    ret = c.get_item('key')
    assert ret['result'] == 'value'
    return ret

@switchcache.twice
def _test_class_with_attr():
    class Test:
        CACHE_PREFIX = 'test:'
        @cache_it(debug=True)
        def get_item(self, key):
            return 'value'
    c = Test()
    ret = c.get_item('key')
    assert ret['result'] == 'value'
    return ret

@raises(ValueError)
def test_class_no_prefix():
    @cache_it(debug=True)
    def get_item(key):
        value = {'hoge': 'fuga'}
        return value
    ret = get_item('key')
    return ret

@switchcache.no_cache
def _test(f):
    ret1, ret2 = f()
    assert ret1['is_cache'] == False
    assert ret2['is_cache'] == True

def test_normal(): _test(_test_normal)
def test_unicode_prefix(): _test(_test_unicode_prefix)
def test_unicode_key(): _test(_test_unicode_key)
def test_multibyte_prefix(): _test(_test_multibyte_prefix)
def test_multibyte_key(): _test(_test_multibyte_key)
def test_with_json_coder(): _test(_test_with_json_coder)
def test_class(): _test(_test_class)
def test_class_with_attr(): _test(_test_class_with_attr)
