# -*- coding: utf-8 -*-

from nose.tools import raises
from cache_it import cache_it, init_cache, cache
import switchcache

def setup():
    init_cache(['invalidhost:12345'])    

@cache_it(prefix='PREFIX', ignore_exception=False)
def get_item_with_exception(key):
    return 'value'

@cache_it(prefix='PREFIX', ignore_exception=True)
def get_item_no_exception(key):
    return 'value'

@raises(Exception)    
def test_with_exception():
    get_item_with_exception('hoge')

@switchcache.no_cache
def test_no_exception():
    assert get_item_no_exception('hoge') == 'value'
    
    
