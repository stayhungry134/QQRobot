"""
name: __init__.py.py
create_time: 2023-02-08
author: Ethan

Description: 
"""
import requests
import datetime
from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import FriendMessage, GroupMessage, MessageEvent
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image, Voice
from graia.ariadne.message.parser.base import MatchRegex, DetectPrefix
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graiax import silkcoder
from modules import headers


def get_iciba():
    """请求爱词霸的每日一句"""
    # https://sentence.iciba.com/index.php?c=dailysentence&m=getdetail&title=2023-02-05
    url = 'https://sentence.iciba.com/index.php'
    today = datetime.date.today()
    data = {
        'c': 'dailysentence',
        'm': 'getdetail',
        'title': today.isoformat(),
    }
    response = requests.get(url=url, params=data, headers=headers).json()
    content = response.get('content')
    note = response.get('note')
    picture_url = response.get('picture2')
    picture_bytes = requests.get(url=picture_url, headers=headers).content
    picture = MessageChain([Image(data_bytes=picture_bytes)])
    voice_url = response.get('tts')
    voice_bytes = requests.get(voice_url, headers=headers).content
    audio_bytes = silkcoder.encode(voice_bytes, ios_adaptive=True)
    audio = MessageChain(Voice(data_bytes=audio_bytes))
    return content, note, picture, audio


channel = Channel.current()


@channel.use(ListenerSchema(listening_events=[GroupMessage, FriendMessage], decorators=[DetectPrefix('#每日一句')]))
async def handle_iciba(app: Ariadne, event: MessageEvent):
    content, note, picture, audio = get_iciba()
    await app.send_message(
        event.sender,
        MessageChain([f"每日一句：", picture, f"\n{content}\n\n{note}"])
    )
    await app.send_message(
        event.sender,
        audio
    )
