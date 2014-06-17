cache_it
====

__cache_it__ is a decorator which wraps caching(read/write) routine.
Decorated functions automatically access your memcache and get/set values depending on the situation.
All you have to do is decorate your function by __@cache_it__.


## Basic Usage

```python
>>> from cache_it import init_cache, cache_it

>>> init_cache(['127.0.0.1:11211'])

>>> @cache_it(prefix='PREFIX:')
>>> def cached_function(key):
>>>     return 'value'

>>> cached_function('key')
'value' # cached => key:'PREFIX:key' value:'value'
>>> cached_function('key')
'value' # getting from a cache

```

## As a method
You can decorate not only functions but also methods in the same way.

```python
class User(Document)
    @cache_it(prefix='PREFIX')
    def __getitem__(self, key):
        return user[key]

```

## ignore_exception (False by default)
If you want to ignore exceptions occured when accessing memcache, you have to set "ignore_exception" into True.

```python
@cache_it(prefix='PREFIX', ignore_exception=True)
def cached_function(key):
    return 'value'
    
```


## ttl (24*60*60 sec by default)

```python
@cache_it(prefix='PREFIX', ttl=60) # 60sec
def cached_function(key):
    return 'value'
    
```

## encoder/decoder
Encoders are called before setting a value.
Decoders, on the other hand, are called after getting a value.

```python
@cache_it(prefix='PREFIX',
          encoder=lambda x: x['foo'],
          decoder=lambda x: {'foo': x})
def cached_function(key):
    return {'foo': 'bar'}


```
