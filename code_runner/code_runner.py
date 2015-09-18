import tornado.ioloop
import tornado.web
import tornado.websocket

from router import Router


class PyWarsApi(tornado.websocket.WebSocketHandler):

    def open(self):
        print "WebSocket opened"

    @tornado.web.asynchronous
    def on_message(self, message):
        Router.route(message, callback_socket=self)

    def on_close(self):
        print "WebSocket closed"

    def check_origin(self, origin):
        return True


application = tornado.web.Application([
    (r"/websocket", PyWarsApi)
])

if __name__ == "__main__":
    application.listen(8083)
    tornado.ioloop.IOLoop.instance().start()

