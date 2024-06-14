"""
name: 
create_time: 2024/6/14 16:19
author: Ethan

Description: 每天发送抖音的热榜
"""

import json
import re
import yaml
import lxml.etree as etree
import datetime

import requests
from graia.ariadne import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image
from graia.ariadne.model import Friend

from modules import headers

f = open('config.yaml', 'r', encoding='utf-8').read()
api_key = yaml.load(f, Loader=yaml.FullLoader).get('tianapi_key')
send_target = yaml.load(f, Loader=yaml.FullLoader).get('douyin_hot')


async def send_douyin_hot(app: Ariadne, target=None):
    """发送抖音热榜"""
    url = 'https://apis.tianapi.com/douyinhot/index'
    params = {
        'key': api_key
    }
    response = requests.get(url, params=params).json()
    if response.get('code') != 200:
        return
    hot_list = response.get('result').get('list')
    # 取前 10 条
    hot_list = [hot.get('word') for hot in hot_list[:10]]
    # 创建消息
    message = "今日抖音热搜：\n" + '\n'.join([f'{index + 1}. {hot}' for index, hot in enumerate(hot_list)])
    await app.send_message(
        target,
        MessageChain(message),
    )


async def send_douyin_hot_task(app: Ariadne):
    """定时发送抖音热榜"""
    friends = send_target.get('friends')
    groups = send_target.get('groups')
    for friend in friends:
        friend = app.get_friend(friend)
        await send_douyin_hot(app, friend)
    for group in groups:
        group = app.get_group(group)
        await send_douyin_hot(app, group)