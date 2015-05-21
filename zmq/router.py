#!/usr/bin/env python2
import zmq
import threading
import uuid
import json
import time


def worker(context):
    ident = "worker-%s" % uuid.uuid1()
    sock = context.socket(zmq.REQ)
    sock.setsockopt(zmq.IDENTITY, ident)
    sock.connect("inproc://backend")

    data = ident
    while True:
        sock.send(data)
        event = json.loads(sock.recv())
        client = event["client"]
        payload = event["payload"]
        print "Worker '%s' receive from client '%s' payload: %s" % \
            (ident, client, payload)
        # do something with payload and return result
        time.sleep(10)
        data = json.dumps({"client": client, "payload": "A1"})


def main():
    context = zmq.Context()
    frontend = context.socket(zmq.ROUTER)
    backend = context.socket(zmq.ROUTER)
    frontend.bind("tcp://127.0.0.1:8080")
    backend.bind("inproc://backend")

    workers = {}
    worker_count = 10

    frontends = {}

    poller = zmq.Poller()
    poller.register(backend, zmq.POLLIN)
    poller.register(frontend, zmq.POLLIN)

    def backend_routine(socks):
        if backend in socks and socks[backend] == zmq.POLLIN:
            ident, _, event = backend.recv_multipart()
            if ident == event:
                # initializing workers
                workers[ident] = True
                print "worker '%s' is registered" % ident
            else:
                event = json.loads(event)
                client = event["client"]
                payload = event.get("payload")
                if payload:
                    print "sending payload to client '%s': %s" % \
                        (client, payload)
                    frontend.send_multipart([str(client), "", str(payload)])
                else:
                    print "nothing to send to client '%s'" % client
                workers[ident] = True

    def frontend_routine(socks, available):
        if frontend in socks and socks[frontend] == zmq.POLLIN:
            parts = frontend.recv_multipart()
            ident = _ = payload = None
            print "received to fronted: %s" % parts
            try:
                ident, _, payload = parts
            except:
                try:
                    _1, _2, ident, _, payload = parts               
                except:
                    return
            if ident == payload and ident.startswith("async"):
                # initializing frontends
                frontends[ident] = True
                print "long polling request from '%s'" % ident
            elif ident.startswith("event"):  # from excel to python
                print "event request from '%s'" % ident
                client = "async-" + "-".join(ident.split("-")[1:])
                if frontends.get(client):
                    event = json.dumps({"client": client, "payload": payload})
                    print "sending to worker '%s' payload: %s" % \
                        (available, event)
                    backend.send_multipart([str(available), "", str(event)])
                    workers[available] = False
                    frontends[client] = False
                else:
                    print ("client '%s' is not available, "
                           "could not send payload: %s") % (client, payload)
                frontend.send_multipart([str(ident), "", "OK"])  # fast answer
            else:
                print "unexpected %s: %s" % (ident, payload)

    for _ in xrange(worker_count):
        threading.Thread(target=worker, args=(context,)).start()

    while True:
        socks = dict(poller.poll())
        backend_routine(socks)
        available = filter(lambda x: x[1], workers.items())
        available = available[0][0]
        if available:
            print "available '%s'" % available
            frontend_routine(socks, available)


if __name__ == '__main__':
    main()
