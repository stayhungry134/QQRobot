"""
name: __init__.py.py
create_time: 2023-02-08
author: Ethan

Description: 
"""
import requests
from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import FriendMessage, GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.event.mirai import NudgeEvent
from graia.ariadne.message.element import Image, Voice
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.model import Group, Friend
from graiax import silkcoder


def get_daily_poem():
    """请求每日诗词"""
    url = 'https://v2.jinrishici.com/one.json'
    data = {
        'token': '81xsqzdKLwDpbPHWLCA1qRGDI88FLYqp',
    }
    response = requests.get(url, params=data).json()
    res_data = {}

    if response.get('status') == 'success':
        origin = response.get('data').get('origin')
        res_data['auther'] = origin.get('author')
        res_data['title'] = origin.get('title')
        res_data['dynasty'] = origin.get('dynasty')
        res_data['poem'] = '\n'.join((origin.get('content')))
    else:
        res_data = "请求失败了"
    return res_data