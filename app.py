import os
import sys
import wsgiref.simple_server
from argparse import ArgumentParser

from builtins import bytes

from linebot import (
    LineBotApi, WebhookParser
)

from linebot.exceptions import (
    InvalidSignatureError
)

from linebot.models import *

from linebot.utils import PY3

Channel_Secret = os.getenv('f22ad583bf1918e828c378a0902903fd', None)
Channel_access_token = os.getenv('d51pvCfNquzJxSXnH3c0tKfCfESz+O+bzpODt93BxuZj+kwPyksU6O/jBgRgUWChc8K92dX26r9qdAEUCsYAIb8G3ZX09pB29t26bSqWTile8foNwGzUwi43U1Ae/PL50D0fRtxpK8fPrqIK/mKwsRsgwYf1m9tXTHnc/ZQT38Y=', None)
if Channel_Secret is None :
    print ('Specify LINE_Channel_Secret as environment variable')
    sys.exit(1)
if Channel_access_token is None :
    print ('Specify LINE_Channel_access_token as environment variable')
    sys.exit(1)

line_bot_api = LineBotApi(Channel_access_token)
parser = WebhookParser(Channel_Secret)


def application(environ, start_response):
    if environ['PATH_INFO'] != '/callback':
        start_response('404 NOT Found', [])
        return create_body('Not Found')
    if environ['REQUEST_METHOD'] != 'POST':
        start_response('405 Method Not Allowed', [])
        return create_body('Method Not Allowed')
    signature = environ['HTTP_X_LINE_SIGNATURE']

    wsgi_input = environ['wsgi.input']
    content_length = int(environ['CONTENT_LENGTH'])
    body = wsgi_input.read(content_length).decode('utf-8')

    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        start_response('400 Bad Request', [])
        return create_body('Bad Request')

    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )
    start_response('200 OK', [])
    return create_body('OK')


def create_body(text):
    if PY3:
        return [bytes(text, 'utf-8')]
    else:
        return text

if __name__ == '__main__':
    arg_parser = ArgumentParser(
        usage='Usage: Python ' + __file__ + ' [--port <port>]  [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help = 'port')
    options = arg_parser.parse_args()

    httpd = wsgiref.simple_server.make_server('', options.port, application)
    httpd.serve_forever()
