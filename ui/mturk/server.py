#!/usr/bin/env python3
import os
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs


class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self, *args, **kwargs):
        res = urlparse(self.path)
        self.path = res.path
        self.query = parse_qs(res.query)
        print("%s - %s" % (self.path, self.query))
        if self.path == '/sandbox/mturk':
            self.path = "/dist/test/test.html"
        elif self.path == '/mturk/':
            self.path = "/dist/test/index.html"
        elif self.path.startswith("/mturk/"):
            self.path = self.path.replace("/mturk/", "/dist/test/")
        print(self.path)
        return super(RequestHandler, self).do_GET(*args, **kwargs)

if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    port = 8000
    handler = RequestHandler
    httpd = socketserver.TCPServer(("", port), handler)
    print("serving at port", port)
    httpd.serve_forever()
