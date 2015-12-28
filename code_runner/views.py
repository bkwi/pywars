import json
import pickle
import base64
import os
import sys
import hashlib
import uuid
from string import Template


import tornado.ioloop
from multiprocessing.pool import ThreadPool
from utils import logger


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pywars.settings')

from django.conf import settings


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