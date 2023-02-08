"""
name: main.py
create_time: 2023-02-08
author: Ethan

Description: 
"""
import os
from creart import create
from graia.ariadne.app import Ariadne
from graia.ariadne.connection.config import (
    HttpClientConfig,
    WebsocketClientConfig,
    config,
)
from graia.saya import Saya


saya = create(Saya)

app = Ariadne(
    connection=config(
        1612189091,  # 你的机器人的 qq 号
        "nihaoya123....",  # 填入你的 mirai-api-http 配置中的 verifyKey
        # 以下两行（不含注释）里的 host 参数的地址
        # 是你的 mirai-api-http 地址中的地址与端口
        # 他们默认为 "http://localhost:8080"
        # 如果你 mirai-api-http 的地址与端口也是 localhost:8080
        # 就可以删掉这两行，否则需要修改为 mirai-api-http 的地址与端口
        HttpClientConfig(host="http://localhost:8888"),
        WebsocketClientConfig(host="http://localhost:8888"),
    ),
)


with saya.module_context():
    for root, _, files in os.walk('modules', topdown=False):
        for file in files:
            if file.endswith('.py') and not file.startswith('_'):
                saya.require(f"{root}.{file[:-3]}".replace('\\', '.'))


app.launch_blocking()