import json

from views import Init, TestSolution


class Router(object):

    routes = {
        'init': Init,
        'test_solution': TestSolution
    }

    @classmethod
    def route(cls, message, callback_socket):
        msg = json.loads(message)
        action = msg.get('action')
        cls.routes[action](msg, callback_socket)

