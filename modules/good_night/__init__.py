"""
name: __init__.py
create_time: 2023-03-17
author: Ethan White

Description: 
"""

import os
import requests
import datetime
import yaml
from creart import create
from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import FriendMessage, GroupMessage, MessageEvent
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Voice
from graia.ariadne.message.parser.base import MatchRegex, DetectPrefix
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.scheduler import GraiaScheduler, timers
from graia.scheduler.saya import SchedulerSchema
from graiax import silkcoder

from modules import BASE_DIR

f = open(os.path.join(BASE_DIR, 'config.yaml'), 'r', encoding='utf-8').read()
good_night = yaml.load(f, Loader=yaml.FullLoader).get('good_night')

channel = Channel.current()
sche = create(GraiaScheduler)


@channel.use(ListenerSchema(listening_events=[GroupMessage, FriendMessage], decorators=[DetectPrefix('#给香菜说晚安')]))
async def send_night(app: Ariadne, target: MessageEvent):
    file_path = os.path.join(BASE_DIR, '0_files', 'sister_good_night.mp3')
    audio = silkcoder.encode(file_path, ios_adaptive=True)
    await app.send_message(
        target,
        MessageChain(Voice(data_bytes=audio)),
    )


@channel.use(SchedulerSchema(timers.crontabify("30 23 * * * 00")))
async def send_good_night(app: Ariadne):
    night_friend = good_night.get('night_friend')
    night_group = good_night.get('night_group')
    file_path = os.path.join(BASE_DIR, '0_files', 'sister_good_night.mp3')
    audio = silkcoder.encode(file_path, ios_adaptive=True)
    for friend in night_friend:
        await app.send_friend_message(
            friend,
            MessageChain(Voice(audio))
        )
    for group in night_group:
        await app.send_group_message(
            group,
            MessageChain(Voice(audio))
        )
