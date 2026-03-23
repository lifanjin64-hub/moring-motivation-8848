"""
新闻爬虫模块
从财联社、新浪财经、微博等平台抓取热门财经新闻
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import re


def fetch_cls_news():
    """
    抓取财联社热门新闻
    由于反爬虫限制，这里使用模拟数据
    实际使用时需要配置代理或使用官方 API
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        
        url = 'https://www.cls.cn/'
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        news_list = []
        
        # 查找新闻列表（需要根据实际网站结构调整）
        news_items = soup.select('.depth-news-item')[:5]
        
        for idx, item in enumerate(news_items, 1):
            title_elem = item.select_one('.title-text')
            if title_elem:
                news_list.append({
                    'rank': idx,
                    'title': title_elem.get_text().strip(),
                    'hot': get_hot_label(idx, 'cls')
                })
        
        if news_list:
            return news_list
    except Exception as e:
        print(f"财联社抓取失败：{e}")
    
    # 返回默认新闻数据
    return get_default_cls_news()


def get_default_cls_news():
    """财联社默认新闻数据"""
    return [
        {
            'rank': 1,
            'title': '中央经济工作会议召开 部署 2026 年经济工作',
            'hot': get_hot_label(1, 'cls')
        },
        {
            'rank': 2,
            'title': 'A 股三大指数集体高开 科技股领涨',
            'hot': get_hot_label(2, 'cls')
        },
        {
            'rank': 3,
            'title': '央行：保持流动性合理充裕 支持实体经济发展',
            'hot': get_hot_label(3, 'cls')
        },
        {
            'rank': 4,
            'title': '新能源汽车销量持续增长 产业链迎来新机遇',
            'hot': get_hot_label(4, 'cls')
        },
        {
            'rank': 5,
            'title': '科技创新成为企业发展核心驱动力',
            'hot': get_hot_label(5, 'cls')
        }
    ]


def fetch_sina_news():
    """
    抓取新浪财经热门新闻
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
        
        url = 'https://finance.sina.com.cn/'
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        news_list = []
        
        # 查找新闻列表（需要根据实际网站结构调整）
        news_items = soup.select('.hot-news-item')[:5]
        
        for idx, item in enumerate(news_items, 1):
            title_elem = item.select_one('a')
            if title_elem:
                news_list.append({
                    'rank': idx,
                    'title': title_elem.get_text().strip(),
                    'hot': get_hot_label(idx, 'sina')
                })
        
        if news_list:
            return news_list
    except Exception as e:
        print(f"新浪财经抓取失败：{e}")
    
    # 返回默认新闻数据
    return get_default_sina_news()


def get_default_sina_news():
    """新浪财经默认新闻数据"""
    return [
        {
            'rank': 1,
            'title': '2026 年宏观经济政策展望：稳中求进',
            'hot': get_hot_label(1, 'sina')
        },
        {
            'rank': 2,
            'title': '科技创新赋能产业升级 高质量发展迈出新步伐',
            'hot': get_hot_label(2, 'sina')
        },
        {
            'rank': 3,
            'title': '消费市场持续回暖 内需潜力加速释放',
            'hot': get_hot_label(3, 'sina')
        },
        {
            'rank': 4,
            'title': '数字经济蓬勃发展 新业态新模式不断涌现',
            'hot': get_hot_label(4, 'sina')
        },
        {
            'rank': 5,
            'title': '绿色发展成为企业共识 低碳转型加速推进',
            'hot': get_hot_label(5, 'sina')
        }
    ]


def fetch_weibo_news():
    """
    抓取微博财经热搜
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
        
        url = 'https://s.weibo.com/top/summary'
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        news_list = []
        
        # 查找热搜列表
        news_items = soup.select('.td-02')[:5]
        
        for idx, item in enumerate(news_items, 1):
            title_elem = item.select_one('a')
            hot_elem = item.select_one('.ico')
            if title_elem:
                hot_text = hot_elem.get_text().strip() if hot_elem else ''
                news_list.append({
                    'rank': idx,
                    'title': title_elem.get_text().strip(),
                    'hot': get_hot_label(idx, 'weibo', hot_text)
                })
        
        if news_list:
            return news_list
    except Exception as e:
        print(f"微博抓取失败：{e}")
    
    # 返回默认新闻数据
    return get_default_weibo_news()


def get_default_weibo_news():
    """微博财经热搜默认数据"""
    return [
        {
            'rank': 1,
            'title': '#中国经济稳中向好#',
            'hot': get_hot_label(1, 'weibo')
        },
        {
            'rank': 2,
            'title': '#科技创新驱动发展#',
            'hot': get_hot_label(2, 'weibo')
        },
        {
            'rank': 3,
            'title': '#创业者的坚持与梦想#',
            'hot': get_hot_label(3, 'weibo')
        },
        {
            'rank': 4,
            'title': '#投资理财知识分享#',
            'hot': get_hot_label(4, 'weibo')
        },
        {
            'rank': 5,
            'title': '#职场成长心得#',
            'hot': get_hot_label(5, 'weibo')
        }
    ]


def get_hot_label(rank, source, hot_text=''):
    """
    根据排名和热度生成标签
    """
    if rank == 1:
        return '🔥 爆'
    elif rank == 2:
        return '🔥 热'
    elif rank == 3:
        return '📈 新'
    else:
        return '📈'


def fetch_all_news():
    """
    抓取所有新闻源的数据
    返回结构化的新闻数据
    """
    print("开始抓取新闻...")
    
    news_data = {
        'cls': fetch_cls_news(),
        'sina': fetch_sina_news(),
        'weibo': fetch_weibo_news()
    }
    
    print("新闻抓取完成")
    return news_data


def save_news_to_file(news_data, filepath='data/news.json'):
    """
    保存新闻数据到 JSON 文件
    """
    news_data['update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(news_data, f, ensure_ascii=False, indent=2)
    
    print(f"新闻数据已保存到 {filepath}")


if __name__ == '__main__':
    news = fetch_all_news()
    save_news_to_file(news)
    print(json.dumps(news, ensure_ascii=False, indent=2))
