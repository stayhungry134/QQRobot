"""
name: good_morning.py
create_time: 2023-02-07
author: Ethan

Description: 
"""
import requests
import datetime
from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import FriendMessage, GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.event.mirai import NudgeEvent
from graia.ariadne.message.element import Image, Voice
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.model import Group, Friend
from graiax import silkcoder


def get_weather(city='530114'):
    """用于请求天气"""
    url = 'https://restapi.amap.com/v3/weather/weatherInfo'
    today = datetime.date.today()
    data = {
        'extensions': 'all',
        'city': city,  # 呈贡区
        'key': '4237e1743fe07beffd1fef65ddf52767',
    }
    response = requests.get(url=url, params=data, headers=header).json()
    forecasts = response.get('forecasts')[0]
    weather_data = forecasts.get('casts')[0]
    weather_remark = ''
    wind_remark = ''
    temp_remark = ''
    if '雨' in weather_data.get('dayweather'):
        weather_remark = '，出门请记得带伞'
    elif '晴' in weather_data.get('dayweather'):
        weather_remark = '，请记得做好防晒'
    if int(weather_data.get('daypower')) > 5:
        wind_remark = '，要把你吹成傻X了，快点躲起来'
    if int(weather_data.get('daytemp')) < 20:
        temp_remark = '，有点凉，做好保暖'
    elif int(weather_data.get('daytemp')) > 30:
        temp_remark = '，热死爹了，记得吃大西瓜'
    week_day = ['一', '二', '三', '四', '五', '六', '天']
    result = f"今天是{today.strftime('%Y年%m月%d日')}，星期{week_day[today.weekday()]}。\n{forecasts.get('city')}{weather_data.get('dayweather')}，" \
             f"{weather_data.get('nighttemp')}度到{weather_data.get('daytemp')}度{temp_remark}{weather_remark}。" \
             f"{weather_data.get('daywind')}风{weather_data.get('daypower')}级{wind_remark}。"

    return result



channel = Channel.current()

