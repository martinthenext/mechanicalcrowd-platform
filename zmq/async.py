#!/usr/bin/env python2
import zmq
import sys


def main(ident):
    ident = "async-%s" % ident
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.setsockopt(zmq.IDENTITY, ident)
    socket.connect("tcp://127.0.0.1:8080")
    while True:
        socket.send(ident)
        res = socket.recv()
        print "received: %s" % res


if __name__ == '__main__':
    main(sys.argv[1])