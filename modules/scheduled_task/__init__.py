"""
name: __init__.py
create_time: 2023/9/6 16:11
author: Ethan

Description: 用于查看 LeetCode上面的刷题记录
"""

import os
import json
import datetime
from pprint import pprint

import requests
import yaml

from creart import create
from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import FriendMessage, GroupMessage, MessageEvent
from graia.ariadne.message.parser.base import DetectPrefix, MatchRegex
from graia.ariadne.message.chain import MessageChain
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.scheduler import GraiaScheduler, timers
from graia.scheduler.saya import SchedulerSchema

from .flash_sale import send_dangdang_sale
from .github import send_github_reminder
from .good_night import send_good_night_task, send_good_night
from .leetcode import send_leetcode_reminder
from .weather import send_morning_weather, send_weather_expand
from .douyinhot import send_douyin_hot, send_douyin_hot_task

channel = Channel.current()
sche = create(GraiaScheduler)


# 天气提醒
@channel.use(ListenerSchema(listening_events=[GroupMessage, FriendMessage], decorators=[MatchRegex("^(?!#).+天气.*")]))
async def weather_expand(app: Ariadne, target: MessageEvent, message: MessageChain):
    await send_weather_expand(app, target, message)


@channel.use(SchedulerSchema(timers.crontabify("50 7 * * * 00")))
async def morning_weather(app: Ariadne):
    await send_morning_weather(app)


# 抖音热搜
@channel.use(ListenerSchema(listening_events=[GroupMessage, FriendMessage], decorators=[DetectPrefix('#抖音热搜')]))
async def douyin_hot(app: Ariadne, target: MessageEvent, message: MessageChain):
    await send_weather_expand(app, target, message)


@channel.use(SchedulerSchema(timers.crontabify("00 21 * * * 00")))
async def douyin_hot_task(app: Ariadne):
    await send_douyin_hot_task(app)


# leetcode 提醒
@channel.use(ListenerSchema(listening_events=[GroupMessage, FriendMessage], decorators=[DetectPrefix('#leetcode')]))
async def leetcode_reminder(app: Ariadne, target: MessageEvent):
    """通过命令回复 leetcode 提交情况"""
    await send_leetcode_reminder(app, target=target)


@channel.use(SchedulerSchema(timers.crontabify("30 21 * * * 00")))
async def leetcode_reminder_task(app: Ariadne):
    """每天晚上检查是否提交了 leetcode"""
    await send_leetcode_reminder(app)


# github 提醒
@channel.use(ListenerSchema(listening_events=[GroupMessage, FriendMessage], decorators=[DetectPrefix('#github')]))
async def github_reminder(app: Ariadne, target: MessageEvent):
    """通过命令回复 github 提交情况"""
    await send_github_reminder(app, target=target)


@channel.use(SchedulerSchema(timers.crontabify("00 23 * * * 00")))
async def github_reminder_task(app: Ariadne):
    """每天晚上检查是否提交了 github"""
    await send_github_reminder(app)


# 发送晚安
@channel.use(ListenerSchema(listening_events=[GroupMessage, FriendMessage], decorators=[DetectPrefix('#晚安')]))
async def good_night(app: Ariadne, target: MessageEvent):
    await send_good_night(app, target)


@channel.use(SchedulerSchema(timers.crontabify("30 23 * * * 00")))
async def good_night_task(app: Ariadne):
    await send_good_night_task(app)


# 当当秒杀提醒
@channel.use(ListenerSchema(listening_events=[GroupMessage, FriendMessage], decorators=[DetectPrefix('#当当秒杀')]))
async def dangdang_sale(app: Ariadne, target: MessageEvent):
    await send_dangdang_sale(app, target)


@channel.use(SchedulerSchema(timers.crontabify("00 0 * * * 00")))
async def dangdang_sale_task_0(app: Ariadne):
    await send_dangdang_sale(app)


@channel.use(SchedulerSchema(timers.crontabify("00 10 * * * 00")))
async def dangdang_sale_task_10(app: Ariadne):
    await send_dangdang_sale(app)


@channel.use(SchedulerSchema(timers.crontabify("00 12 * * * 00")))
async def dangdang_sale_task_12(app: Ariadne):
    await send_dangdang_sale(app)


@channel.use(SchedulerSchema(timers.crontabify("00 14 * * * 00")))
async def dangdang_sale_task_14(app: Ariadne):
    await send_dangdang_sale(app)


@channel.use(SchedulerSchema(timers.crontabify("00 16 * * * 00")))
async def dangdang_sale_task_16(app: Ariadne):
    await send_dangdang_sale(app)
