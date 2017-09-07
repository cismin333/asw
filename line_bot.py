from flask import Flask, request, abort
import configparser
import requests


from linebot import (
    LineBotApi, WebhookHandler
)

from linebot.exceptions import (
    InvalidSignatureError
)

from linebot.models import *

app = Flask(__name__)
config = configparser.ConfigParser()
config.read("config.ini")

line_bot_api = LineBotApi(config['line_bot']['Channel_access_token'])
handler = WebhookHandler(config['line_bot']['Channel_secret'])


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'ok'


def line_today():
    target_url = 'https://today.line.me/TW/pc'
    print ('Line Today web page')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    content = ""
    return content


@handler.add(MessageEvent, message=TextMessage)
def handel_message(event):
    print ("event.reply_token:", event.reply_token)
    print ("event.message.text:", event.message.text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )
    if event.message.text == "News":
        content = line_today()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content)
        )
        return 0

    button_template = TemplateSendMessage(
        alt_text='Menu Template',
        template=ButtonsTemplate(
            title='Please Choose an service',
            text='options',
            thumbnail_image_url='https://goo.gl/1CYL7q',
            actions=[
                MessageTemplateAction(
                    label='News',
                    text='News'
                )
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, button_template)
    return 0


if __name__ == "_main_":
    app.run()
