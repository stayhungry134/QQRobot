"""
name: __init__.py.py
create_time: 2023-02-07
author: Ethan

Description:
"""
import requests
from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import FriendMessage, GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import At
from graia.ariadne.message.parser.base import MentionMe, MatchRegex
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.model import Group, Member

channel = Channel.current()


def get_chat(msg):
    """青云客聊天接口"""
    # http://api.qingyunke.com/api.php?key=free&appid=0&msg=%E4%BD%A0%E5%A5%BD
    url = 'http://api.qingyunke.com/api.php'
    data = {
        'key': 'free',
        'appid': 0,
        'msg': msg
    }
    response = requests.get(url=url, params=data).json()
    return response.get('content')


@channel.use(ListenerSchema(listening_events=[GroupMessage], decorators=[MentionMe(), MatchRegex('^[^#]([^天气]*)$')]))
async def handle_grop_chat(app: Ariadne, group: Group, member: Member, message: MessageChain = MentionMe()):
    content = get_chat(message.display)
    await app.send_message(
        group,
        MessageChain(At(member.id), '， ', content)
    )


@channel.use(ListenerSchema(listening_events=[FriendMessage], decorators=[MatchRegex('^[^#]([^天气]*)$')]))
async def handle_chat(app: Ariadne, message: MessageChain, friend_message: FriendMessage):
    """朋友发消息的时候聊天"""
    content = get_chat(message.display).replace('{br}', '\n')
    await app.send_friend_message(
        friend_message.sender,
        MessageChain(content)
    )