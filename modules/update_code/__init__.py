"""
name: __init__.py
create_time: 2023-02-14
author: Ethan White

Description: 通过命令更新代码
"""
import os
import yaml
from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.event.message import FriendMessage
from graia.ariadne.message.parser.base import MatchRegex
from graia.ariadne.model import Friend
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from modules import BASE_DIR


f = open(os.path.join(BASE_DIR, 'config.yaml'), 'r', encoding='utf-8').read()
master_id = yaml.load(f, Loader=yaml.FullLoader).get('master_id')


channel = Channel.current()


@channel.use(ListenerSchema(listening_events=[FriendMessage], decorators=[MatchRegex('^#更新代码$')]))
async def update_self(app: Ariadne, friend: Friend):
    print(friend.id)
    print(master_id, type(master_id))
    if friend.id == master_id:
        await app.send_friend_message(
            friend,
            MessageChain("更新成功！")
        )
        os.system('source /root/QQ/qq.sh')
