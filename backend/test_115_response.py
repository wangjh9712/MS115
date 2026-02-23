"""
测试 115 API 返回数据结构
"""
import asyncio
from p115client import P115Client
import json
import os
from dotenv import load_dotenv

load_dotenv()

# 从环境变量获取 cookie
cookie = os.getenv('PAN115_COOKIE', '')
print(f"Cookie length: {len(cookie) if cookie else 0}")
print(f"Cookie preview: {cookie[:30]}...{cookie[-20:] if len(cookie) > 50 else cookie}")

if not cookie or cookie == 'your_115_cookie_here':
    print("\n请先在 .env 文件中配置 PAN115_COOKIE")
    exit(1)

async def test_api():
    client = P115Client(cookie)
    
    print("\n" + "="*50)
    print("测试 user_info API")
    print("="*50)
    try:
        result = await client.user_info(async_=True)
        print("Response keys:", result.keys() if isinstance(result, dict) else type(result))
        if isinstance(result, dict) and 'data' in result:
            print("data keys:", result['data'].keys())
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "="*50)
    print("测试 user_space_info API")
    print("="*50)
    try:
        result = await client.user_space_info(async_=True)
        print("Response keys:", result.keys() if isinstance(result, dict) else type(result))
        if isinstance(result, dict) and 'data' in result:
            print("data keys:", result['data'].keys())
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}")

    print("\n" + "="*50)
    print("测试 fs_index_info API")
    print("="*50)
    try:
        result = await client.fs_index_info(async_=True)
        print("Response keys:", result.keys() if isinstance(result, dict) else type(result))
        if isinstance(result, dict) and 'data' in result:
            print("data keys:", result['data'].keys())
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}")

asyncio.run(test_api())