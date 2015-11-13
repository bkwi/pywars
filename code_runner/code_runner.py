import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.escape

from router import Router

connections = {
    # 'user_id': [conn1, conn2, ...]
}

class PyWarsWebsocket(tornado.websocket.WebSocketHandler):

    def open(self):
        user_id = self.request.query
        connections.setdefault(user_id, [])
        connections.get(user_id).append(self)
        print "CONNECTIONS", connections

    @tornado.web.asynchronous
    def on_message(self, message):
        Router.route(message, callback_socket=self)

    def on_close(self):
        user_id = self.request.query
        if self in connections.get(user_id):
            connections.get(user_id).remove(self)

    def check_origin(self, origin):
        return True


class WebsocketApi(tornado.web.RequestHandler):

    def get(self):
        self.write("Hello, world")

    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        user_id = data.get('user_id')
        if user_id:
            for conn in connections.get(user_id, []):
                conn.write_message({'abc': 'woohoo'})
        self.write('ok')


application = tornado.web.Application([
    (r"/websocket", PyWarsWebsocket),
    (r"/test", WebsocketApi)
])

if __name__ == "__main__":
    application.listen(8083)
    tornado.ioloop.IOLoop.instance().start()

