"""
name: 
create_time: 2024/4/11 16:14
author: Ethan

Description: 用于发送秒杀活动提醒
"""
import json
import re
import yaml
import lxml.etree as etree

import requests
from graia.ariadne import Ariadne
from graia.ariadne.message import MessageChain
from graia.ariadne.message.element import Image

from modules import headers

f = open('config.yaml', 'r', encoding='utf-8').read()
master = yaml.load(f, Loader=yaml.FullLoader).get('master_id')

async def send_dangdang_sale(app: Ariadne, target=None):
    """发送当当网的秒杀活动"""
    url = 'https://miao.dangdang.com/'
    response = requests.get(url, headers=headers).content.decode('gbk')
    # 获取活动id
    activity_id = re.search(r'mixActivity(\d+)', response).group(1)
    data = {
        'current': '0',
        'activity': json.dumps({"activityId": activity_id}),
    }
    miaosha = requests.post(
        'https://miao.dangdang.com/Standard/Miaosha/Core/hosts/getActivityProducts.php',
        headers=headers,
        data=data,
    ).content.decode('gbk')

    html = etree.HTML(miaosha)
    # 获取秒杀的书籍
    items = html.xpath('//ul[@class="sale"]/li')
    book_list = []
    for item in items:
        title = item.xpath('.//a[@class="name"]/text()')[0]
        price = item.xpath('.//p[@class="price"]/span/text()')[0]
        cover_url = item.xpath('.//a[@class="show"]/img/@src')[0]
        cover_bytes = requests.get(cover_url, headers=headers).content
        cover = MessageChain(Image(data_bytes=cover_bytes))
        book_list.extend([title, price, cover, "\n"])



    pre_msg = f"当当网正在秒杀以下书籍：\n"
    await app.send_friend_message(
        target if target else master,
        MessageChain([pre_msg, *book_list])
    )

