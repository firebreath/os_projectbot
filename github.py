#!/usr/bin/env python
"""
github.py - Phenny Github Module
Copyright 2011, Richard Bateman
Licensed under the New BSD License.

Written for use in the #firebreath IRC channel: http://www.firebreath.org
"""

from github2.client import Github
import re
import web

gh = Github()

def f_find_github_commit(phenny, input):
    print "Searching for commit...", input
    query = input.group(1)
    _find_github_commit(phenny, query)

def _find_github_commit(phenny, query):
    try:
        res = gh.commits.show(phenny.config.github_project, sha=query)
        print res
        phenny.say("%s by %s: %s %s" % (res.id[:7], res.author["name"], res.message[:60], shorten("https://github.com" + res.url)))
    except:
        print "Couldn't find %s" % query
        pass

f_find_github_commit.rule = r'.*\b([0-9a-f]{7,40})\b.*'
f_find_github_commit.priority = "low"
f_find_github_commit.thread = True

def f_find_github_file(phenny, input):
    print "Searching for file: ", input
    tmp = input.group(1).strip().split(" ", 1)
    if len(tmp) > 1:
        _find_github_file(phenny, tmp[0], tmp[1])
    else:
        _find_github_file(phenny, phenny.config.github_defaultbranch, tmp[0])

def _find_github_file(phenny, branch, fname):
    bag = web.json(web.get("https://github.com/api/v2/json/blob/all/%s/%s" % (phenny.config.github_project, branch)))["blobs"]
    outlist = [f for f in bag.keys() if re.search(fname.lower(), f.lower())]
    outlist.sort()
    if outlist:
        phenny.say ("Found %s matching file(s) in the %s branch. First %s are:" % (len(outlist), branch), min(5, len(outlist)))
        for found in outlist[:5]:
            url = "https://github.com/%s/tree/%s%s" % (phenny.config.github_project, branch, found)
            url = shorten(url)
            phenny.say("%s %s" % (found, url))

f_find_github_file.rule = r'\.findfile (.*)'
f_find_github_file.priority = "low"
f_find_github_file.thread = True

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
