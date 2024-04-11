"""
name: 
create_time: 2024/4/11 15:32
author: Ethan

Description: 用于请求 LeetCode上面的刷题记录
"""
import datetime
import json
import os
import yaml
import requests


from graia.ariadne.message.chain import MessageChain

from modules import BASE_DIR, headers

f = open(os.path.join(BASE_DIR, 'config.yaml'), 'r', encoding='utf-8').read()
leet_code_config = yaml.load(f, Loader=yaml.FullLoader).get('leet_code')
leet_id = leet_code_config.get('username')

api_url = 'https://leetcode.cn/graphql/noj-go/'

headers['referer'] = f'https://leetcode-cn.com/u/{leet_id}/'

query_dic = {
    'userProfileCalendar': '\n    query userProfileCalendar($userSlug: String!, $year: Int) {\n  userCalendar(userSlug: $userSlug, year: $year) {\n    streak\n    totalActiveDays\n    submissionCalendar\n    activeYears\n    monthlyMedals {\n      name\n      obtainDate\n      category\n      config {\n        icon\n        iconGif\n        iconGifBackground\n      }\n      progress\n      id\n      year\n      month\n    }\n    recentStreak\n  }\n}\n    ',
    'recentAcSubmissions': '\n    query recentAcSubmissions($userSlug: String!) {\n  recentACSubmissions(userSlug: $userSlug) {\n    submissionId\n    submitTime\n    question {\n      title\n      translatedTitle\n      titleSlug\n      questionFrontendId\n    }\n  }\n}\n    ',
    'languageStats': '\n    query languageStats($userSlug: String!) {\n  userLanguageProblemCount(userSlug: $userSlug) {\n    languageName\n    problemsSolved\n  }\n}\n    ',
    'problemSolvedBeatsStats': '\n    query problemSolvedBeatsStats($userSlug: String!) {\n  problemsSolvedBeatsStats(userSlug: $userSlug) {\n    difficulty\n    percentage\n  }\n}\n    ',

}
classify_dic = {
    '提交日历': 'userProfileCalendar',
    '最近提交': 'recentAcSubmissions',
    '语言统计': 'languageStats',
    '问题统计': 'problemSolvedBeatsStats'
}


def get_leet_code(leet_code_id, key):
    """获取 leet_code 上面的代码提交记录"""
    # 提交日历
    key = classify_dic.get(key)
    json_data = {
        'query': query_dic.get(key),
        'variables': {
            'userSlug': leet_code_id,
        },
        'operationName': key,
    }

    response = requests.post(url=api_url, json=json_data, headers=headers).json()
    return response


async def send_leetcode_reminder(app, target=None):
    master = leet_code_config.get('master')
    today = datetime.date.today()

    # 提交日历
    leet_calendar = get_leet_code(leet_id, '提交日历')
    submit_calender = json.loads(leet_calendar.get('data').get('userCalendar').get('submissionCalendar'))
    # 最后一次提交的日期
    last_date = datetime.datetime.fromtimestamp(int(list(submit_calender.keys())[-1])).date()
    last_date_str = last_date.isoformat()
    # 提交数列表
    submit_list = list(submit_calender.values())
    # 近一年提交的天数
    submit_counter = len(submit_list)
    # 总提交数
    all_submit = sum(submit_list)

    # 最近提交
    leet_recent = get_leet_code(leet_id, '最近提交')
    # 最近提交的题目
    recent_problem = leet_recent.get('data').get('recentACSubmissions')[0].get('question')
    # 最近提交的题号
    recent_problem_id = recent_problem.get('questionFrontendId')
    # 最近提交的题目标题
    recent_problem_title = recent_problem.get('translatedTitle')

    # 问题统计
    # leet_problem = get_leet_code(leet_id, '问题统计')
    # # 问题统计列表
    # problem_list = leet_problem.get('data').get('problemsSolvedBeatsStats')
    # stas_str = f"简单题：{problem_list[0].get('percentage')}%\n" \

    push_remark = "你今天还没有提交 leet_code，"
    last_submit = f"上一次提交日期为 {last_date_str}\n\n"
    # 如果今天提交过
    if last_date == today:
        push_remark = "你今天提交了 leet_code"
        last_submit = "\n\n"

    reminder_content = f"{push_remark}{last_submit}" \
                       f"近一年中你有{submit_counter}天提交了代码，总提交数{all_submit}\n\n" \
                       f"最近一次提交的题目为 {recent_problem_id}题{recent_problem_title}"

    await app.send_friend_message(
        target if target else master,
        MessageChain(reminder_content)
    )

