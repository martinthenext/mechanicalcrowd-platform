#!/usr/bin/env python2
import zmq
import time

def main(wait=False):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://127.0.0.1:8080")
    while True:
        message = socket.recv()
        print "Received request: ", message
        
        if wait:
            print "Waiting 10 seconds before responding"
            time.sleep(10)
            print "Response sent"

        socket.send("OK")

if __name__ == '__main__':
    main()

