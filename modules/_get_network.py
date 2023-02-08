"""
name: _get_network.py
create_time: 2023-02-05
author: Ethan

Description: 用于请求网络资源
"""
import requests
import datetime

header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}


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
    response = requests.get(url=url, params=data, headers=header).json()
    content = response.get('content')
    note = response.get('note')
    picture = response.get('picture2')
    pronunciation = response.get('tts')

    return content, note, picture, pronunciation


def get_daily_poem():
    """请求每日诗词"""
    url = 'https://v2.jinrishici.com/one.json'
    data = {
        'token': '81xsqzdKLwDpbPHWLCA1qRGDI88FLYqp',
    }
    response = requests.get(url, params=data, headers=header).json()
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