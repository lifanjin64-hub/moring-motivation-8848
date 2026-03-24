"""
主更新脚本
整合新闻和励志内容，更新 HTML 文件
"""

import json
import os
import sys
from datetime import datetime
from bs4 import BeautifulSoup

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.fetch_news import fetch_all_news
from scripts.generate_content import get_daily_content


def load_html_template():
    """加载 HTML 模板"""
    with open('index.html', 'r', encoding='utf-8') as f:
        return f.read()


def generate_news_html(news_data):
    """生成新闻 HTML 片段 - 综合财经热点排名"""
    html = ''
    
    # 综合财经热点排名
    html += '''
            <div class="news-source">
                <div class="news-source-header comprehensive">
                    <span class="icon">📰</span>
                    <h3>综合财经热点 TOP10</h3>
                </div>
                <ul class="news-list">
'''
    for item in news_data.get('comprehensive', []):
        rank_class = get_rank_class(item['rank'])
        source_info = f" <span class=\"source-tag\">{item.get('source', '')}</span>" if item.get('source') else ""
        html += f'''
                    <li class="news-item">
                        <span class="rank {rank_class}">{item['rank']}</span>
                        <span class="title">{item['title']}{source_info}</span>
                        <span class="hot {get_hot_class(item['hot'])}">{item['hot']}</span>
                    </li>
'''
    html += '''
                </ul>
            </div>
'''
    
    return html


def get_rank_class(rank):
    """获取排名样式类"""
    if rank == 1:
        return 'top1'
    elif rank == 2:
        return 'top2'
    elif rank == 3:
        return 'top3'
    else:
        return 'normal'


def get_hot_class(hot_text):
    """获取热度样式类"""
    if '爆' in hot_text or '🔥' in hot_text:
        return 'hot-red'
    elif '热' in hot_text:
        return 'hot-red'
    elif '新' in hot_text:
        return 'hot-orange'
    else:
        return 'hot-orange'


def generate_content_html(daily_content):
    """生成励志内容 HTML 片段"""
    quote = daily_content['quote']
    story = daily_content['story']
    message = daily_content['message']
    
    # 构建故事段落
    story_paragraphs = ''
    for paragraph in story['content']:
        story_paragraphs += f'''
                <p>
                    {paragraph.replace(story['highlight'], f'<span class="highlight">{story["highlight"]}</span>')}
                </p>
'''
    
    return {
        'date': daily_content['date'],
        'weekday': daily_content['weekday'],
        'quote_text': quote['text'],
        'quote_author': quote['author'],
        'story_title': story['title'],
        'story_content': story_paragraphs,
        'message_title': message['title'],
        'message_content': message['content']
    }


def update_html(news_data, daily_content):
    """更新 HTML 文件"""
    html_template = load_html_template()
    soup = BeautifulSoup(html_template, 'html.parser')
    
    # 更新日期
    date_elem = soup.select_one('#currentDate')
    if date_elem:
        date_elem.string = daily_content['date']
    
    weekday_elem = soup.select_one('#currentDay')
    if weekday_elem:
        weekday_elem.string = daily_content['weekday']
    
    # 更新金句
    quote_elem = soup.select_one('.quote')
    if quote_elem:
        quote_elem.string = daily_content['quote_text']
    
    quote_author = soup.select_one('.quote-author')
    if quote_author:
        quote_author.string = f"— {daily_content['quote_author']}"
    
    # 更新历史故事
    story_section = soup.select_one('.content-section')
    if story_section:
        story_title = story_section.select_one('h3')
        if story_title:
            story_title.string = f"🏮 {daily_content['story_title']}"
        
        # 更新故事内容
        content_p = story_section.select('p')
        if content_p and len(content_p) >= 2:
            for i, p in enumerate(content_p[:2]):
                if i < len(daily_content['story_content'].strip().split('</p>')) - 1:
                    p.replace_with(BeautifulSoup(daily_content['story_content'].strip().split('</p>')[i] + '</p>', 'html.parser'))
    
    # 更新创业寄语
    encouragement_section = soup.select('.content-section')[1] if len(soup.select('.content-section')) > 1 else None
    if encouragement_section:
        message_p = encouragement_section.select('p')
        if message_p:
            # 分割消息内容为多行
            message_lines = daily_content['message_content'].split('。')
            for i, p in enumerate(message_p):
                if i < len(message_lines):
                    text = message_lines[i] + '。' if i < len(message_lines) - 1 else message_lines[i]
                    p.string = text.strip()
    
    # 更新行动建议
    encouragement_card = soup.select_one('.encouragement-card')
    if encouragement_card:
        card_text = encouragement_card.select_one('.encouragement-text')
        if card_text:
            card_text.string = daily_content['message_content']
    
    # 更新新闻模块
    news_section = soup.select_one('.news-section')
    if news_section:
        # 更新更新时间
        update_time = news_section.select_one('#updateTime')
        if update_time:
            update_time.string = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        # 更新新闻列表 - 综合财经热点
        news_sources = news_section.select('.news-source')
        if news_sources:
            # 更新综合财经热点
            update_news_source(news_sources[0], news_data.get('comprehensive', []))
    
    # 保存更新后的 HTML
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    print("HTML 文件已更新")


def update_news_source(source_elem, news_items):
    """更新新闻源列表"""
    news_list = source_elem.select_one('.news-list')
    if news_list and news_items:
        news_list.clear()
        for item in news_items:
            rank_class = get_rank_class(item['rank'])
            source_info = f' <span class="source-tag">{item.get("source", "")}</span>' if item.get('source') else ""
            li = BeautifulSoup(f'''
                <li class="news-item">
                    <span class="rank {rank_class}">{item['rank']}</span>
                    <span class="title">{item['title']}{source_info}</span>
                    <span class="hot {get_hot_class(item['hot'])}">{item['hot']}</span>
                </li>
            ''', 'html.parser')
            news_list.append(li)


def main():
    """主函数"""
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    print("=" * 50)
    print("开始更新晨间励志网站内容")
    print("=" * 50)
    
    # 获取每日励志内容
    print("\n[1/3] 生成每日励志内容...")
    daily_content = get_daily_content()
    print(f"[OK] 日期：{daily_content['date']} {daily_content['weekday']}")
    print(f"[OK] 金句：{daily_content['quote']['text'][:20]}...")
    print(f"[OK] 故事：{daily_content['story']['title']}")
    
    # 获取新闻数据
    print("\n[2/3] 抓取热门新闻...")
    news_data = fetch_all_news()
    print(f"[OK] 综合财经新闻：{len(news_data.get('comprehensive', []))} 条")
    
    # 保存新闻数据
    news_data['update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M')
    with open('data/news.json', 'w', encoding='utf-8') as f:
        json.dump(news_data, f, ensure_ascii=False, indent=2)
    print("[OK] 新闻数据已保存到 data/news.json")
    
    # 更新 HTML
    print("\n[3/3] 更新 HTML 文件...")
    content_html = generate_content_html(daily_content)
    update_html(news_data, content_html)
    
    print("\n" + "=" * 50)
    print("[OK] 更新完成！")
    print("=" * 50)
    
    return True


if __name__ == '__main__':
    main()
