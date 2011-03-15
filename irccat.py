#!/usr/bin/env python
"""
irccat.py - Phenny "irccat" Module
Copyright 2011, Richard Bateman
Licensed under the New BSD License.

Written to be used in the #firebreath IRC channel: http://www.firebreath.org
"""

import SocketServer, thread
from SocketServer import ThreadingMixIn, StreamRequestHandler

shared_data = {}

class IrcCatListener(ThreadingMixIn, StreamRequestHandler):
    def handle(self):
        phenny = shared_data["phenny"]
        msg = self.rfile.readline().strip()

        print "Handling communication"
        print "Received", msg

        dest, msg = self.splitMsg(msg)
        if not dest:
            dest = phenny.channels
        print "Channels:", dest

        for chan in dest:
            if chan[0] == "#" and chan in phenny.channels:
                print "Someone tried to make me say something in a channel I'm not in!"
            else:
                phenny.msg(chan, msg)

    def splitMsg(self, message):
        if message[0] not in ('#', '@'):
            return [], message

        dest, message = message.split(" ", 1)
        dest = [x.strip().strip("@") for x in dest.split(",")]
        return dest, message

def startListener():
    print "-- irccat thread started"
    HOST, PORT = shared_data["phenny"].config.irccat_host, shared_data["phenny"].config.irccat_port
    server = SocketServer.TCPServer((HOST, PORT), IrcCatListener)
    print "-- starting irccat server on %s:%s" % (HOST, PORT)
    server.serve_forever()
    print "closing thread?"

def setup(phenny):
    print "-- setting up irccat..."
    shared_data["phenny"] = phenny
    thread.start_new_thread(startListener, tuple())

