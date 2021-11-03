# Create your views here.
from os import access
from imgurpython import ImgurClient
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, PostbackEvent, ImageSendMessage

from .scraper import bulletin

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):

    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)  # 傳入的事件
            print(events)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        event_now = ""
        for event in events:
            if isinstance(event, PostbackEvent):
                print("--------------------------------")
                print(event.postback.data)
                if event.postback.data == "1":
                    line_bot_api.reply_message(
                        event.reply_token, TextSendMessage(text="postback1"))
                elif event.postback.data == "2":
                    line_bot_api.reply_message(
                        event.reply_token, TextSendMessage(text="postback2"))
                elif event.postback.data == "3":
                    line_bot_api.reply_message(
                        event.reply_token, TextSendMessage(text="Account:"))
                    event_now = "act"
                    if isinstance(event, MessageEvent):
                        act = event.message.text
                        line_bot_api.reply_message(
                            event.reply_token, TextSendMessage(text="Password:"))
                        if isinstance(event, MessageEvent):
                            pwd = event.message.text
                            line_bot_api.reply_message(
                                event.reply_token, TextSendMessage(text=act+pwd))
                            line_bot_api.reply_message(
                                event.reply_token, ImageSendMessage(
                                    original_content_url='https://i.imgur.com/uCtZt9i.png',
                                    preview_image_url='https://i.imgur.com/uCtZt9i.png'
                                ))
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                if event.message.text == "sc":
                    line_bot_api.reply_message(
                        event.reply_token, TextSendMessage(text=bulletin(1).scrape()))
                elif event_now == "act":
                    act = event.message.text
                    line_bot_api.reply_message(
                        event.reply_token, TextSendMessage(text="Password:"))
                    event_now = "pwd"
                elif event_now == "pwd":
                    pwd = event.message.text
                    line_bot_api.reply_message(
                        event.reply_token, TextSendMessage(text=act+pwd))
                    event_now = ""
                else:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(
                        text=event.message.text))  # 回復傳入的訊息文字
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
