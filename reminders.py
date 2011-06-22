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
lmgt.example = '.lmgt swhack'

def bothelp(phenny, input):
    phenny.say("Bot help -- most used commands:")
    phenny.say("!findfile <regex> - Search for files in the project tree on github")
    phenny.say("!find <symbol> - use ctags to search for a symbol in the source tree")
    phenny.say("!wiki <search string> - search the wiki for the given string")
    phenny.say("git pull requests - list all open pull requests for the project")
    phenny.say(".pb - remind users about pastebin services")
    phenny.say(".ask - remind users to ask their question rather than waiting for someone to come")
    phenny.say(".g <search string> - search google for <search string> and return the url of the first response")
    phenny.say(".lmgt <search string> - display 'Let me Google that for you' link for <search string>")
    phenny.say(".extensions - Display a summary of the difference between a plugin and an extension.")

bothelp.commands = ['bothelp']
bothelp.priority = "medium"

def extensions(phenny, input):
    phenny.say("Browser plugins vs extensions: Plugins live in an <object> tag and only interact with the DOM.")
    phenny.say("They don't hook into any special events with the browser, aren't given special web browser info.")
    phenny.say("They cannot automatically affect a page without being inserted into said page.")
    phenny.say("Note that FireBreath plugins can often be used as part of an extension.")
    phenny.say("For more information about the difference between a plugin and extension, see http://npapi.com/extensions")

extensions.commands = ["extensions"]
extensions.priority = "medium"
