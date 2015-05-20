#!/usr/bin/env python2
import zmq
import sys

def main(ident, event):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    ident = "event-%s" % ident
    socket.setsockopt(zmq.IDENTITY, ident)
    socket.connect("tcp://127.0.0.1:8080")
    print "sending event from '%s': %s" % (ident, event)
    socket.send(event)
    res = socket.recv()
    print "received: %s" % res

if __name__ == '__main__':
    ident, event = sys.argv[1:3]
    main(ident, event)