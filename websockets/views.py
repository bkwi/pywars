import uuid
from utils import logger


class WebSocketResponseException(Exception):
    pass


class WebSocketResponse(object):

    response = None

    def __init__(self, msg, callback_socket):
        self.msg = msg
        self.msg_id = uuid.uuid4().hex
        logger.debug("Websocket message - id: %s, body: %s",
                     self.msg_id, msg)
        self.callback_socket = callback_socket
        self.perform()

    def perform(self):
        self.send_response()

    def send_response(self):
        if self.response is None:
            raise WebSocketResponseException('No response defined')
        logger.debug('Websocket response to %s: %s', self.msg_id,
                     self.response)
        self.callback_socket.write_message(self.response)


class Init(WebSocketResponse):
    response = {'action': 'init', 'msg': 'ok'}