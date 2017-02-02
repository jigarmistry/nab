import json
import tornado.ioloop
import tornado.web

command = ""


class WebHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", title="NAB")

    def post(self):
        global command
        data = tornado.escape.json_decode(self.request.body)
        command = data["command"]
        self.write(json.dumps({"command": command}))


class NeatHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Neat Handler Server")

    def post(self):
        self.write(command)


def make_app():
    return tornado.web.Application(
        [
            (r"/web", WebHandler),
            (r"/neat", NeatHandler),
        ], debug=True)


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Server Running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()