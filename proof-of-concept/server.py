#!/usr/bin/env python
import uuid
from hashlib import md5
import tornado.ioloop
import tornado.web
import argparse
import sys


class AnalyzerHandler(tornado.web.RequestHandler):
    def get_action(self):
        return self.request.body_arguments["action"][0]

    def get_column_name(self):
        return self.request.body_arguments["column"][0]

    def get_column_id(self, colname):
        return colname.__hash__()

    def prepare_json(self, col_id, action):
        json = {"doc_col_id": col_id, "action": action, "data": []}
        cells = []
        for cell, values in sorted(self.request.body_arguments.items()):
            if cell in ["action", "column"]:
                continue
            value = values[0] if values else ""
            if action == "check_new":
                json["data"].append(value)
                cells.append(cell)
            elif action == "cell_unmarked":
                json["data"] = value
                cells.append(cell)
            elif action == "cell_corrected":
                json["data"] += values
                cells.append(cell)
            else:
                self.set_status(400)
                self.finish()
                return None, None
        return json, cells

    def analyze(self, action, json):
        VARIANTS = ["DONTKNOWN", "INCORRECT", "CORRECT"]
        result = online_query(json)
        if action in ("check_new", "check_old"):
            return map(lambda x: VARIANTS[x + 1], result)
        return [VARIANTS[2]]

    def post(self):
        print("ARGS: %s" % self.request.body_arguments.items())
        action = self.get_action()
        col_id = self.get_column_id(self.get_column_name())
        json, cells = self.prepare_json(col_id, action)
        if json is None:
            return
        print("JSON:\n%s\n" % json)
        result = self.analyze(action, json)
        if result:
            result = "&".join(map(lambda x: "%s=%s" % x, zip(cells, result)))
            print("RESULT: %s" % result)
            self.write(result)
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


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-P", "--pythonpath", default=".")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    sys.path.append(args.pythonpath)
    from online_query import online_query

    application = load_application()
    application.listen(8000, address="127.0.0.1")
    tornado.ioloop.IOLoop.instance().start()
