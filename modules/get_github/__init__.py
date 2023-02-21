"""
name: __init__.py
create_time: 2023-02-14
author: Ethan White

Description: 用于请求
"""
import os
import re
import datetime
import requests
import yaml

from creart import create
from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import FriendMessage, GroupMessage, MessageEvent
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.parser.base import DetectPrefix
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.scheduler import GraiaScheduler, timers
from graia.scheduler.saya import SchedulerSchema

from modules import BASE_DIR, headers

f = open(os.path.join(BASE_DIR, 'config.yaml'), 'r', encoding='utf-8').read()
github_config = yaml.load(f, Loader=yaml.FullLoader).get('github')


def get_github(github_id):
    """获取 github 上面的代码提交记录"""
    url = f"https://github.com/{github_id}"
    response = requests.get(url=url, headers=headers).text
    level_list = re.findall(r'data-date="(.*)"\sdata-level="(\d)"*', response)
    level_dic = {key: int(value) for key, value in level_list}
    # 返回 {日期: 贡献值} 的字典
    return level_dic


channel = Channel.current()
sche = create(GraiaScheduler)


async def send_reminder(app, target=None, check=False):
    github_id = github_config.get('username')
    master = github_config.get('master')
    level_dic = get_github(github_id)
    today = datetime.date.today().isoformat()
    # 总贡献
    sum_contribution = sum(level_dic.values())
    # 近一年提交的天数
    contribution_list = [k for k, v in level_dic.items() if v > 0]
    contribution_counter = len(contribution_list)
    last_push = contribution_list[-1]

    if check:
        if level_dic.get(today) == 0:
            reminder_content = f"你今天还没有提交 github，上一次提交日期为 {last_push}\n\n" \
                               f"近一年中你有{contribution_counter}天提交了代码，总贡献数{sum_contribution}"
            await app.send_message(
                target if target else master,
                MessageChain(reminder_content)
            )
    else:
        push_remark = "你今天还没有提交 github"
        if level_dic.get(today) > 0:
            push_remark = "你今天提交了 github"
        reminder_content = f"{push_remark}，上一次提交日期为 {last_push}\n\n" \
                           f"近一年中你有{contribution_counter}天提交了代码，总贡献数{sum_contribution}"
        await app.send_message(
            target if target else master,
            MessageChain(reminder_content)
        )


@channel.use(ListenerSchema(listening_events=[GroupMessage, FriendMessage], decorators=[DetectPrefix('#github')]))
async def github_reminder(app: Ariadne, target: MessageEvent):
    """通过命令回复 github 提交情况"""
    await send_reminder(app, target=target)


@channel.use(SchedulerSchema(timers.crontabify("00 23 * * * 00")))
async def send_github_reminder(app: Ariadne):
    """每天晚上检查是否提交了 github"""
    check = True
    await send_reminder(app, check=check)


