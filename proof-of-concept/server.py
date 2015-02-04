#!/usr/bin/env python
import uuid
from hashlib import md5
import tornado.ioloop
import tornado.web


def analyze(value):
    if value.isdigit():
        digit = int(value)
        if digit % 2 == 0:
            return "OK"
        else:
            return "FAIL"
    else:
        return "DNK"


class AnalyzerHandler(tornado.web.RequestHandler):
    def post(self):
        result = []
        for cell, values in self.request.body_arguments.items():
            if cell in ["type"]:
                continue
            value = values[0] if values else ""
            result.append("%s=%s" % (cell, analyze(value)))
        output = "&".join(result)
        self.write(output)
        self.set_status(200)


def load_application():
    application = tornado.web.Application(
        [
            (r'/analyzer', AnalyzerHandler),
        ],
        gzip=False,
        xsrf_cookies=False,
        cookie_secret=md5(uuid.uuid1().bytes).hexdigest())
    return application


if __name__ == '__main__':
    application = load_application()
    application.listen(8000, address="127.0.0.1")
    tornado.ioloop.IOLoop.instance().start()
