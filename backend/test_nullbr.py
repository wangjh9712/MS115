"""
Nullbr API 测试脚本
使用新的通用客户端
"""
import os

# 设置环境变量
os.environ["NULLBR_APP_ID"] = "Jy19cpz9p"
os.environ["NULLBR_API_KEY"] = "rIxTz7XHDEHBcP9lGpeVAgs0I7Evg6wc"
os.environ["NULLBR_BASE_URL"] = "https://api.nullbr.eu.org/"

from app.services.nullbr_service import NullbrService


def main():
    service = NullbrService()

    print("=== 搜索测试 ===")
    try:
        result = service.search("银翼杀手")
        print(f"Total results: {result.get('total_results', 'N/A')}")
        items = result.get("items", [])[:3]
        for item in items:
            print(f"  {item.get('title')} ({item.get('release_date')}) - 评分: {item.get('vote_average')}")
        print("\n搜索 API 测试成功!")
    except Exception as e:
        print(f"搜索 Error: {e}")

    print("\n=== 电影详情测试 ===")
    try:
        result = service.get_movie(78)
        print(f"Title: {result.get('title')}")
        print(f"Has 115: {result.get('115-flg')}")
        print("电影详情 API 测试成功!")
    except Exception as e:
        print(f"电影详情 Error: {e}")

    print("\n=== 用户信息测试 ===")
    try:
        result = service.get_user_info()
        print(f"Subscription: {result.get('data', {}).get('sub_name')}")
        print(f"Daily used: {result.get('data', {}).get('daily_used')}/{result.get('data', {}).get('daily_quota')}")
        print("用户信息 API 测试成功!")
    except Exception as e:
        print(f"用户信息 Error: {e}")


if __name__ == "__main__":
    main()
