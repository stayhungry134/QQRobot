"""
name: command.py
create_time: 2023-02-05
author: Ethan

Description: 用于执行指令
"""
from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import FriendMessage, GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.event.mirai import NudgeEvent
from graia.ariadne.message.element import Image, Voice
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.model import Group, Friend
from graiax import silkcoder

channel = Channel.current()


# 此处注释的意思是用法类比，不是说这里可以用 GroupMessage
# @channel.use(ListenerSchema(listening_events=[GroupMessage]))
@channel.use(ListenerSchema(listening_events=[NudgeEvent]))
async def handle_nudge(app: Ariadne, event: NudgeEvent):
    if event.context_type == "group":
        await app.send_group_message(
            event.group_id,
            MessageChain("你不要光天化日之下在这里戳我啊")
        )
    elif event.context_type == "friend":
        await app.send_friend_message(
            event.friend_id,
            MessageChain("别戳我，好痒！")
        )
    else:
        return


# 天气预报
@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def handle_command(app: Ariadne, message: MessageChain, group: Group):
    flag = 'normal'
    if message.display == '#天气预报' and flag == 'normal':
        from ._get_network import get_weather
        weather = get_weather()
        await app.send_message(
            group,
            MessageChain(weather)
        )
    if message.display == '#每日一句' and flag == 'normal':
        import requests
        from ._get_network import get_iciba
        content, note, picture, pronunciation = get_iciba()
        audio = requests.get(pronunciation).content
        audio_bytes = await silkcoder.async_encode(audio, ios_adaptive=True)
        await app.send_group_message(
            group,
            MessageChain(f"每日一句：", Image(url=picture), f"\n{content}\n\n{note}\n\n记得认真学习哦！")
        )
        await app.send_group_message(
            group,
            MessageChain(Voice(data_bytes=audio_bytes))
        )
    if message.display == '#每日诗词' and flag == 'normal':
        from ._get_network import get_daily_poem
        poem_data = get_daily_poem()
        if isinstance(poem_data, dict):
            await app.send_group_message(
                group,
                MessageChain(f"{poem_data.get('title'):^40}\n"
                             f"{poem_data.get('auther') + '(' + poem_data.get('dynasty'):>40})\n"
                             f"{poem_data.get('poem'):^40}")
            )
        else:
            await app.send_group_message(
                group,
                MessageChain(poem_data)
            )
    if message.display == '#开始聊天':
        flag = 'chat'
        if flag == 'chat':
            from ._get_network import get_chat
            content = get_chat(message.display)
            await app.send_group_message()

    elif message.display == '#结束聊天':
        flag = 'normal'

# @channel.use(ListenerSchema(listening_events=[]))
# TODO 有电视剧更新的时候提醒我
# TODO B 站追番之后更新提醒