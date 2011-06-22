#!/usr/bin/python
"""
reminders.py - Common reminders for visitors
"""

from os_projectbot.shorten import shorten
import web

def ask(phenny,input):
    s = "If you need help, just ask your question and wait for people to come back."
    phenny.say(s)

ask.commands = ["ask"]
ask.priority = "medium"

def pb(phenny,input):
    s = "When you need to share code, logs, or anything else longer than a couple of lines, use a pastebin. http://fpaste.org, https://pzt.me/, and https://gist.github.com are all good options"
    phenny.say(s)

pb.commands = ["pb", "pastebin"]
pb.priority = "medium"

def lmgt(phenny, input): 
    """Queries Google for the specified input."""
    a= "http://lmgtfy.com/?q=download+solr"
    query = input.group(2)
    url = "http://lmgtfy.com/?q=%s" % web.urllib.quote(query.encode('utf-8'))
    phenny.say("Let me google that for you: %s" % shorten(url))
lmgt.commands = ['lmgt']
lmgt.priority = 'high'
lmgt.example = '.g swhack'
