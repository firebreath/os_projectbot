#!/usr/bin/env python
"""
github.py - Phenny Github Module
Copyright 2011, Richard Bateman
Licensed under the New BSD License.

Written for use in the #firebreath IRC channel: http://www.firebreath.org
"""

from github2.client import Github

gh = Github()

def f_find_github_commit(self, input):
    print "Searching for commit...", input
    query = input.group(1)
    _find_github_commit(self, query)

def _find_github_commit(self, query):
    try:
        res = gh.commits.show(self.config.github_project, sha=query)
        print res
        self.say("%s by %s: %s %s" % (res.id[:7], res.author["name"], res.message[:60], shorten("https://github.com" + res.url)))
    except:
        print "Couldn't find %s" % query
        pass

f_find_github_commit.rule = r'.*\b([0-9a-f]{7,40})\b.*'
f_find_github_commit.priority = "low"
f_find_github_commit.thread = True

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
