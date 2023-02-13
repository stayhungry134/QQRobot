"""
name: __init__.py.py
create_time: 2023-02-07
author: Ethan

Description:
"""
import os
from typing import Union
import yaml
import requests
import datetime
import yaml
from creart import create
from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import FriendMessage, GroupMessage, MessageEvent
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.parser.base import MatchRegex, DetectPrefix
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.scheduler import GraiaScheduler, timers
from graia.scheduler.saya import SchedulerSchema

from modules import BASE_DIR

f = open(os.path.join(BASE_DIR, 'config.yaml'), 'r', encoding='utf-8').read()
weather = yaml.load(f, Loader=yaml.FullLoader).get('weather')


def get_weather(city=weather.get('city'), index=0):
    """用于请求天气"""
    url = 'https://restapi.amap.com/v3/weather/weatherInfo'
    today = datetime.date.today()
    data = {
        'extensions': 'all',
        'city': city,  # 呈贡区
        'key': weather.get('key'),
    }
    if city == "请求失败了！":
        return city
    response = requests.get(url=url, params=data).json()
    forecasts = response.get('forecasts')[0]
    weather_data = forecasts.get('casts')[index]
    date_remake = ''
    weather_remark = ''
    wind_remark = ''
    temp_remark = ''
    if index:
        year, month, day = weather_data.get('date').split('-')
        date_remake = f"{year}年{month}月{day}日"
    if '雨' in weather_data.get('dayweather'):
        weather_remark = '，出门请记得带伞'
    elif '晴' in weather_data.get('dayweather'):
        weather_remark = '，请记得做好防晒'
    if weather_data.get('daypower') != '≤3' and int(weather_data.get('daypower')) > 5:
        wind_remark = '，要把你吹成傻X了，快点躲起来'
    if int(weather_data.get('daytemp')) < 20:
        temp_remark = '，有点凉，做好保暖'
    elif int(weather_data.get('daytemp')) > 30:
        temp_remark = '，热死爹了，记得吃大西瓜'
    week_day = ['一', '二', '三', '四', '五', '六', '天']
    result = f"今天是{today.strftime('%Y年%m月%d日')}，星期{week_day[today.weekday()]}。\n" \
             f"{forecasts.get('city')}{date_remake}{weather_data.get('dayweather')}，" \
             f"{weather_data.get('nighttemp')}度到{weather_data.get('daytemp')}度{temp_remark}{weather_remark}。" \
             f"{weather_data.get('daywind')}风{weather_data.get('daypower')}级{wind_remark}。"

    return result


def get_city(address):
    """用于请求城市编码"""
    # https://restapi.amap.com/v3/geocode/geo?address = 北京市朝阳区阜通东大街6号 & output = XML & key = < 用户的key >
    url = 'https://restapi.amap.com/v3/geocode/geo'
    data = {
        'address': address,
        'key': weather.get('key'),
    }
    response = requests.get(url, params=data).json()
    if response.get('status') == '0':
        return "请求失败了！"
    city = response.get('geocodes')[0]
    adcode = city.get('adcode')
    return adcode


channel = Channel.current()
sche = create(GraiaScheduler)


@channel.use(ListenerSchema(listening_events=[GroupMessage, FriendMessage], decorators=[DetectPrefix('#今日天气')]))
async def send_weather(app: Ariadne, target: MessageEvent):
    today_weather = get_weather()
    await app.send_message(
        target,
        MessageChain(today_weather),
    )


@channel.use(ListenerSchema(listening_events=[GroupMessage, FriendMessage], decorators=[MatchRegex("^(?!#).+天气.*")]))
async def send_weather_expand(app: Ariadne, target: MessageEvent, message: MessageChain):
    weather_message = message.display
    address = weather_message.split('天气')[0]
    date_index = 0
    if address[-1] == '天':
        date = address[-2:]
        address = address[:-2]
        if date in ['明天', '二天']:
            date_index = 1
        if date in ['后天', '三天']:
            date_index = 2
            if address[-1] == '大':
                date_index = 3
    city = get_city(address)
    city_weather = get_weather(city, index=date_index)
    await app.send_message(
        target,
        MessageChain(city_weather),
    )


@channel.use(SchedulerSchema(timers.crontabify("50 7 * * * 00")))
async def send_morning_weather(app: Ariadne):
    morning_weather = get_weather()
    morning_friend = weather.get('morning_friend')
    morning_group = weather.get('morning_group')
    for friend in morning_friend:
        await app.send_friend_message(
            friend,
            MessageChain(morning_weather)
        )
    for group in morning_group:
        await app.send_group_message(
            group,
            MessageChain(morning_weather)
        )
