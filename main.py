"""
name: main.py
create_time: 2023-02-08
author: Ethan

Description: 
"""
import os
import yaml
from creart import create
from graia.ariadne.app import Ariadne
from graia.ariadne.connection.config import (
    HttpClientConfig,
    WebsocketClientConfig,
    config,
)
from graia.saya import Saya
f = open("config.yaml", 'r', encoding='utf-8').read()
cfg = yaml.load(f, Loader=yaml.FullLoader).get('config')
saya = create(Saya)

app = Ariadne(
    connection=config(
        cfg.get('qq_id'),  # 你的机器人的 qq 号
        cfg.get('verifyKey'),  # 填入你的 mirai-api-http 配置中的 verifyKey
        # 是你的 mirai-api-http 地址中的地址与端口
        # 他们默认为 "http://localhost:8080"
        # 如果你 mirai-api-http 的地址与端口也是 localhost:8080
        # 就可以删掉这两行，否则需要修改为 mirai-api-http 的地址与端口
        HttpClientConfig(host=cfg.get('address')),
        WebsocketClientConfig(host=cfg.get('address')),
    ),
)


with saya.module_context():
    for file in os.listdir('modules'):
        if not file.startswith('_'):
            if file.endswith('.py'):
                file = file[:-3]
            saya.require(f"modules.{file}")


app.launch_blocking()