#!/usr/bin/env python2
import zmq


def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://127.0.0.1:8080")
    while True:
        message = socket.recv()
        print "Received request: ", message 
        socket.send("OK")


if __name__ == '__main__':
    main()

