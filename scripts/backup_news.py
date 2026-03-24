"""
备用新闻源模块
当主要新闻源失败时，使用这些备用 API
"""

import requests
import json


def fetch_from_guokr_api():
    """
    使用果壳网 API 获取科技新闻
    """
    try:
        url = 'https://www.guokr.com/beta/api/flow'
        params = {
            'limit': 5,
            'category': 'science'
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        news_list = []
        
        if 'result' in data:
            for idx, item in enumerate(data['result'][:5], 1):
                title = item.get('title', '')
                if title:
                    news_list.append({
                        'rank': idx,
                        'title': title.strip(),
                        'hot': get_hot_label(idx)
                    })
        
        return news_list if news_list else None
    except Exception as e:
        print(f"果壳 API 失败：{e}")
        return None


def fetch_from_zhihu_daily():
    """
    使用知乎日报 API
    """
    try:
        url = 'https://daily.zhihu.com/api/4/news/latest'
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        news_list = []
        
        if 'stories' in data:
            for idx, item in enumerate(data['stories'][:5], 1):
                title = item.get('title', '')
                if title:
                    news_list.append({
                        'rank': idx,
                        'title': title.strip(),
                        'hot': get_hot_label(idx)
                    })
        
        return news_list if news_list else None
    except Exception as e:
        print(f"知乎日报 API 失败：{e}")
        return None


def get_hot_label(rank):
    """生成热度标签"""
    if rank == 1:
        return '[HOT] 爆'
    elif rank == 2:
        return '[HOT] 热'
    elif rank == 3:
        return '[NEW] 新'
    else:
        return '[UP]'


if __name__ == '__main__':
    print("测试备用新闻源...")
    
    print("\n1. 测试果壳 API:")
    guokr_news = fetch_from_guokr_api()
    if guokr_news:
        for news in guokr_news:
            print(f"  {news['rank']}. {news['title']} {news['hot']}")
    else:
        print("  失败")
    
    print("\n2. 测试知乎日报 API:")
    zhihu_news = fetch_from_zhihu_daily()
    if zhihu_news:
        for news in zhihu_news:
            print(f"  {news['rank']}. {news['title']} {news['hot']}")
    else:
        print("  失败")
