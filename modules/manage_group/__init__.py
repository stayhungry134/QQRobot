"""
name: __init__.py
create_time: 7/20/2023 5:01 PM
author: Ethan

Description: 
"""

from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import FriendMessage, GroupMessage, MessageEvent
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.parser.base import MatchRegex, DetectPrefix, MatchContent, RegexGroup, Mention
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

channel = Channel.current()


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def recall_violation_message(app: Ariadne, target: MessageEvent, message: MessageChain):
    import re
    import logging
    content = message.display
    at_pattern = '[@][1-9][0-9]{7,10}'
    pattern = '(?:加群|[1-9][0-9]{7,10}|兼职|群号|微信号)'
    # 如果是 @ 或者回复别人
    if re.search(at_pattern, content):
        return
    elif re.search(pattern, content):
        try:
            await app.recall_message(
                target
            )
        except:
            logging.error(f'撤回{content}失败')
    pass
