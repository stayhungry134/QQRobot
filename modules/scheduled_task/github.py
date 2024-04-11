"""
name: 
create_time: 2024/4/11 16:05
author: Ethan

Description: 
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
from graia.ariadne.message.element import Plain
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
    try:
        response = requests.get(url=url, headers=headers).text
    except Exception as e:
        return "请求 github 失败了！"
    level_list = re.findall(r'data-date="(\w{4}-\w{2}-\w{2})".*data-level="(\w)"*', response)
    level_dic = {key: int(value) for key, value in level_list}
    # 将 level_dic 按照转换为日期的键排序
    level_dic = dict(sorted(level_dic.items(), key=lambda x: datetime.datetime.strptime(x[0], '%Y-%m-%d')))
    # 返回 {日期: 贡献值} 的字典
    return level_dic


async def send_github_reminder(app: Ariadne, target=None):
    github_id = github_config.get('username')
    master = github_config.get('master')
    level_dic = get_github(github_id)
    if isinstance(level_dic, str):
        await app.send_friend_message(
            target if target else master,
            MessageChain(Plain(level_dic)),
        )
        return

    today = datetime.date.today().isoformat()
    # 总贡献
    sum_contribution = sum(level_dic.values())
    # 近一年提交的天数
    contribution_list = [k for k, v in level_dic.items() if v > 0]
    contribution_counter = len(contribution_list)
    last_push = contribution_list[-1]

    push_remark = "你今天还没有提交 github"
    if level_dic.get(today) > 0:
        push_remark = "你今天提交了 github"
    reminder_content = f"{push_remark}，上一次提交日期为 {last_push}\n\n" \
                       f"近一年中你有{contribution_counter}天提交了代码，总贡献数{sum_contribution}"
    await app.send_friend_message(
        target if target else master,
        MessageChain(reminder_content),
    )


