#!/usr/bin/env python
"""
github.py - Phenny Github Module
Copyright 2011, Richard Bateman
Licensed under the New BSD License.

Written for use in the #firebreath IRC channel: http://www.firebreath.org
"""

from github2.client import Github
from os_projectbot.shorten import shorten
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
        phenny.say ("Found %s matching file(s) in the %s branch. First %s are:" % (len(outlist), branch, min(5, len(outlist))))
        for found in outlist[:5]:
            fnd = found.strip("/")
            url = "https://github.com/%s/tree/%s/%s" % (phenny.config.github_project, branch, fnd)
            url = shorten(url)
            phenny.say("%s %s" % (found, url))

f_find_github_file.rule = r'\!findfile (.*)'
f_find_github_file.priority = "low"
f_find_github_file.thread = True

#
# List tagfiles
#
def f_list_git_pull_requests(phenny, input):
    prList = web.json(web.get("http://github.com/api/v2/json/pulls/%s/open" % phenny.config.github_project))
    pulls = prList["pulls"]
    if len(pulls) == 0:
        phenny.say("There are no open pull requests in %s" % phenny.config.github_project)
    else:
        phenny.say("%s open pull request%s:" % (len(pulls), "s" if len(pulls) != 1 else ""))
        for issue in pulls:
            title = issue["title"][:60]
            if len(issue["title"]) > 60: title += "..."
            phenny.say("%s: %s %s" % (issue["user"]["login"], title, shorten(issue["html_url"])))
f_list_git_pull_requests.rule = r'^git pull request'
f_list_git_pull_requests.priority = "medium"
f_list_git_pull_requests.thread = True

#
# Tagfile lookup
#

def f_find_github_tag(phenny, input):
    print "Searching for tag: ", input
    tmp = input.group(1).strip().split(" ", 2)
    if len(tmp) > 1:
        _find_github_tag(phenny, tmp[1], tmp[0].split(","))
    else:
        _find_github_tag(phenny, tmp[0])

def getTag(e):
    r = {}
    for n in ("name", "file", "pattern", "lineNumber", "kind", "fileScope"):
        r[n] = e[n]
    return r

def _find_github_tag(phenny, fname, types=("c", "f", "t")):
    import ctags
    from ctags import CTags, TagEntry

    t = CTags(phenny.config.tagfile)
    e = TagEntry()
    if not t.find(e, fname, ctags.TAG_PARTIALMATCH):
        phenny.say("Could not find any tags matching %s" % fname)
        return
    tags = [getTag(e)]
    while t.findNext(e):
        if e["kind"] in types:
            tags.append(getTag(e))

    newtags = []
    for e in tags:
        if e not in newtags: newtags.append(e)

    phenny.say("Found %s possible matches. Displaying %s" % (len(newtags), min(len(newtags), 5)))

    for entry in tags[:5]:
        url = "https://github.com/%s/tree/%s/%s" % (phenny.config.github_project, "master", entry["file"])
        if entry["lineNumber"]:
            url += "#%s" % entry["lineNumber"]
        url = shorten(url)
        phenny.say("%s (%s) found in %s: %s" % (entry["pattern"], entry["kind"], entry["file"], url))

f_find_github_tag.rule = r'\!find (.*)'
f_find_github_tag.priority = "low"
f_find_github_tag.thread = True

#!/usr/bin/python
# use Google's http://goo.gl/ URL shortener
# requires urllib, urllib2, re, simplejson
# This is shamelessly borrowed from http://segfault.in/2010/10/shorten-urls-using-google-and-python/
