from django.http import HttpResponseRedirect, HttpResponse

import inotify.adapters
import time
import subprocess as sp
import json
import asyncio

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer
from channels.consumer import AsyncConsumer

from django_eventstream import send_event

def ws_connect(message):
    message.reply_channel.send({
        'accept' : True
    })

def ws_disconnect(message):
    pass

def message_handler(message):
    text = message.content['text']
    request = json.loads(text)
    _path = '/tmp'
    exe_task.delay()

    message.reply_channel.send({'text': 'done'})

    return

    fm = file_monitor.delay(_path)
    fm.get(on_message=on_raw_message)
    res = fm.get()
    for k in range(100):
        if 'IN_MODIFY' in res:
            tail_of_lines = sp.run(['tail', '-n1', '/var/log/messages'], stdout=sp.PIPE)
            result_data = tail_of_lines.stdout.decode('utf-8')
            message.reply_channel.send({
                'text' : result_data
            })

    return

    chk_times = 10
    while chk_times == 10:
        time.sleep(1)

        fm = file_monitor.delay(_path)
        fm.get(on_message=on_raw_message)
        res = fm.get()

        if 'IN_MODIFY' in res:
            tail_of_lines = sp.run(['tail', '-n1', '/tmp/demo'], stdout=sp.PIPE)
            result_data = tail_of_lines.stdout.decode('utf-8').strip('\n')
            message.reply_channel.send({
                'text' : result_data
            })

            print(result_data)

        if 'IN_MODIFY' in res:
            with open('/var/log/messages', 'r') as _fff:
                ll = _fff.readlines()
                for ii in ll:
                    message.reply_channel.send({
                        'text': ii
                    })

    message.reply_channel.send({'text': 'done'})

    return

    if request['id'] == '001':
        pass

def on_raw_message(body):
    print(body)

def file_detector(thefile):
    thefile.seek(0, 2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line