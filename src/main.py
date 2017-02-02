import json
import tornado.ioloop
import tornado.web

command = ""
web_reply = {}


class WebHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", title="NAB")

    def post(self):
        global command
        data = tornado.escape.json_decode(self.request.body)
        command = data["command"]
        self.write(json.dumps(web_reply))


class NeatHandler(tornado.web.RequestHandler):
    def get(self):
        server = str(self.get_query_argument("server"))
        player = str(self.get_query_argument("player"))
        time = str(self.get_query_argument("time"))
        city = str(self.get_query_argument("city"))
        print("NEAT [GET] -->  Player : " + player + " Server : " + server +
              " Time : " + time)
        n_resp = "OKAY"
        if command:
            n_resp = command
        self.write(n_resp)

    def post(self):
        global web_reply
        data = tornado.escape.json_decode(self.request.body)
        print("NEAT [POST] --> " + json.dumps(data))
        web_reply = data
        self.write("OKAY")


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