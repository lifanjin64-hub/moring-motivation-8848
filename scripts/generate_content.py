"""
每日励志内容生成模块
根据日期选择不同的金句、历史故事和创业寄语
"""

import json
from datetime import datetime
import hashlib


def load_json_data(filepath):
    """加载 JSON 数据文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_daily_quote(quotes_data, date=None):
    """
    根据日期选择每日金句
    使用日期哈希确保每天的内容固定
    """
    if date is None:
        date = datetime.now()
    
    date_str = date.strftime('%Y-%m-%d')
    hash_value = int(hashlib.md5(date_str.encode()).hexdigest(), 16)
    
    quotes = quotes_data['quotes']
    index = hash_value % len(quotes)
    
    return quotes[index]


def get_daily_story(stories_data, date=None):
    """
    根据日期选择每日历史故事
    """
    if date is None:
        date = datetime.now()
    
    date_str = date.strftime('%Y-%m-%d')
    hash_value = int(hashlib.md5(date_str.encode()).hexdigest(), 16)
    
    stories = stories_data['stories']
    index = hash_value % len(stories)
    
    return stories[index]


def get_daily_message(messages_data, date=None):
    """
    根据日期选择每日行动建议
    """
    if date is None:
        date = datetime.now()
    
    date_str = date.strftime('%Y-%m-%d')
    hash_value = int(hashlib.md5(date_str.encode()).hexdigest(), 16)
    
    messages = messages_data['messages']
    index = hash_value % len(messages)
    
    return messages[index]


def get_daily_content(date=None):
    """
    获取完整的每日励志内容
    """
    if date is None:
        date = datetime.now()
    
    # 加载数据
    quotes_data = load_json_data('data/quotes.json')
    stories_data = load_json_data('data/stories.json')
    messages_data = load_json_data('data/messages.json')
    
    # 获取每日内容
    quote = get_daily_quote(quotes_data, date)
    story = get_daily_story(stories_data, date)
    message = get_daily_message(messages_data, date)
    
    return {
        'date': date.strftime('%Y年%m月%d日'),
        'weekday': get_weekday(date),
        'quote': quote,
        'story': story,
        'message': message
    }


def get_weekday(date):
    """获取中文星期"""
    weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    return weekdays[date.weekday()]


def generate_daily_content():
    """生成并保存每日励志内容"""
    content = get_daily_content()
    
    # 保存为 JSON 文件
    with open('data/daily_content.json', 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=2)
    
    print("每日励志内容已生成")
    print(f"日期：{content['date']} {content['weekday']}")
    print(f"金句：{content['quote']['text'][:30]}...")
    print(f"故事：{content['story']['title']}")
    print(f"行动建议：{content['message']['content'][:30]}...")
    
    return content


if __name__ == '__main__':
    generate_daily_content()
