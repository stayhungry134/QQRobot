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

from modules import BASE_DIR

f = open(os.path.join(BASE_DIR, 'config.yaml'), 'r', encoding='utf-8').read()
github_config = yaml.load(f, Loader=yaml.FullLoader).get('github')


def get_github(github_id):
    """获取 github 上面的代码提交记录"""
    url = f"https://github.com/{github_id}"
    cookies = {
        '_octo': 'GH1.1.1180550844.1712673213',
        '_device_id': '6e423e10886da2b741dbc8953a1e10bf',
        'saved_user_sessions': '57486694%3A6v_NcuiWpPTCVVcXgHgBuIG7B44wLdvIvnCmfS2bSy1f2P1v',
        'user_session': '6v_NcuiWpPTCVVcXgHgBuIG7B44wLdvIvnCmfS2bSy1f2P1v',
        '__Host-user_session_same_site': '6v_NcuiWpPTCVVcXgHgBuIG7B44wLdvIvnCmfS2bSy1f2P1v',
        'logged_in': 'yes',
        'dotcom_user': 'stayhungry134',
        'color_mode': '%7B%22color_mode%22%3A%22auto%22%2C%22light_theme%22%3A%7B%22name%22%3A%22light%22%2C%22color_mode%22%3A%22light%22%7D%2C%22dark_theme%22%3A%7B%22name%22%3A%22dark%22%2C%22color_mode%22%3A%22dark%22%7D%7D',
        'preferred_color_mode': 'light',
        'tz': 'Asia%2FShanghai',
        'has_recent_activity': '1',
        '_gh_sess': 'tK7CXctwhxFTRrWPElulpxoRzlnZT%2BkjkzrTo9FEebKn58j65t%2FZVRbKtXEN1SojkorCRiIjO1k9Mp2TCv9GLQs1iVEjMMgsl%2B2kG9Ay2T4vyFRRhCO9GBhQXcEMPjctPcO4QjD2fhPZcepOGXmuD5htj9WUx545qLkCWQEr4Kb3r0k00Y9as7MA1gbc6yjMc%2FOb3BeHi9YOpQJ%2FDmRBG79k7rt6G1VJvDZFdxXXHtaGqSdjJawjC4wL9i1VQp8pipiGd9zCfGqXez2Ny2X0sPnYO0N4QlTWSXQ%2FycG5%2BXtsFONbK9YGA94mjpUETSWmSxOBohx82GW6LURaNb2yXRzv1vfB84XHEUn9kw%3D%3D--qyEZkVi2uJqnUhr6--1WYDi19VhlyJrow%2FGH9Vhg%3D%3D',
    }
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-CN,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-GB;q=0.6,en-US;q=0.5',
        'cache-control': 'max-age=0',
        'if-none-match': 'W/"5dc92dd33dd38b4e7728637650aedb1f"',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    }
    params = {
        'action': 'show',
        'controller': 'profiles',
        'tab': 'contributions',
        'user_id': 'stayhungry134',
    }
    try:
        response = requests.get(url=url, headers=headers, cookies=cookies, params=params).text
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


