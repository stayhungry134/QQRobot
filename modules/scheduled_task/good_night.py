"""
name: 
create_time: 2024/4/11 16:10
author: Ethan

Description: 
"""
import os

import yaml
from graia.ariadne import Ariadne
from graia.ariadne.event.message import MessageEvent
from graia.ariadne.message import MessageChain
from graia.ariadne.message.element import Voice
from graiax import silkcoder

from modules import BASE_DIR


async def send_good_night(app: Ariadne, target: MessageEvent):
    file_path = os.path.join(BASE_DIR, '0_files', 'sister_good_night.mp3')
    audio = silkcoder.encode(file_path, ios_adaptive=True)
    await app.send_message(
        target,
        MessageChain(Voice(data_bytes=audio)),
    )

f = open(os.path.join(BASE_DIR, 'config.yaml'), 'r', encoding='utf-8').read()
good_night_target = yaml.load(f, Loader=yaml.FullLoader).get('good_night')


async def send_good_night_task(app: Ariadne):
    night_friend = good_night_target.get('night_friend')
    night_group = good_night_target.get('night_group')
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