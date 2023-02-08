"""
name: good_morning.py
create_time: 2023-02-02
author: Ethan White

Description: 用于测试
"""
import requests
from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.saya import Channel
from graia.ariadne.message.element import Image, Voice
from graia.scheduler import timers
from graia.scheduler.saya import SchedulerSchema
from ._get_network import get_iciba, get_weather
from graiax import silkcoder


channel = Channel.current()

content, note, picture, pronunciation = get_iciba()
weather = get_weather()


@channel.use(SchedulerSchema(timers.crontabify("30 8 * * * 0")))
async def good_morning(app: Ariadne):
    audio = requests.get(pronunciation).content
    audio_bytes = await silkcoder.async_encode(audio, ios_adaptive=True)
    await app.send_group_message(
        1028709782,
        MessageChain(f"群友们大家好，{weather}")
    )
    await app.send_group_message(
        1028709782,
        MessageChain(f"每日一句：", Image(url=picture), f"\n{content}\n\n{note}\n\n记得认真学习哦！")
    )
    await app.send_group_message(
        1028709782,
        MessageChain(Voice(data_bytes=audio_bytes))
    )