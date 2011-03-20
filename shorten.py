#!/usr/bin/python
# use Google's http://goo.gl/ URL shortener
# requires urllib, urllib2, re, simplejson
# This is shamelessly borrowed from http://segfault.in/2010/10/shorten-urls-using-google-and-python/
def shorten(url):
    try:
        from re import match
        from urllib2 import urlopen, Request, HTTPError
        from urllib import quote
        from json import loads
    except ImportError, e:
        raise Exception('Required module missing: %s' % e.args[0])
    if not match('http://',url) and not match('https://', url):
        raise Exception('URL must start with "http://"')
    try:
        a = urlopen(Request('http://goo.gl/api/url','url=%s'%quote(url),{'User-Agent':'toolbar'}))
        j = loads(a.read())
        return j["short_url"]
    except HTTPError, e:
        j = loads(e.read())
        print j
        if 'short_url' not in j:
            try:
                from pprint import pformat
                j = pformat(j)
            except ImportError:
                j = j.__dict__
            raise Exception('Didn\'t get a correct-looking response. How\'s it look to you?\n\n%s'%j)
        return j['short_url']
    raise Exception('Unknown eror forming short URL.')

