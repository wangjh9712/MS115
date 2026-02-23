"""
Nullbr API 完整测试脚本
"""
import os
import sys

# 设置环境变量
os.environ.setdefault("NULLBR_APP_ID", "Jy19cpz9p")
os.environ.setdefault("NULLBR_API_KEY", "rIxTz7XHDEHBcP9lGpeVAgs0I7Evg6wc")
os.environ.setdefault("NULLBR_BASE_URL", "https://api.nullbr.com/")

from app.services.nullbr_service import NullbrService

service = NullbrService()

results = []

def test(name, func, *args, **kwargs):
    try:
        result = func(*args, **kwargs)
        results.append((name, "OK", result))
        print(f"[OK] {name}")
        return result
    except Exception as e:
        results.append((name, "FAIL", str(e)))
        print(f"[FAIL] {name}: {e}")
        return None

print("=" * 50)
print("Nullbr API Test")
print("=" * 50)

print("\n--- META Interfaces (APP_ID only) ---")
test("search", service.search, "busan")
test("get_list", service.get_list, 2142788)
test("get_movie", service.get_movie, 78)
test("get_tv", service.get_tv, 1396)
test("get_tv_season", service.get_tv_season, 1396, 1)
test("get_tv_episode", service.get_tv_episode, 1396, 1, 1)
test("get_person", service.get_person, 57607)
test("get_collection", service.get_collection, 295)

print("\n--- RES Interfaces (APP_ID + API_KEY) ---")
test("get_movie_115", service.get_movie_pan115, 78)
test("get_movie_magnet", service.get_movie_magnet, 78)
test("get_movie_ed2k", service.get_movie_ed2k, 78)
test("get_movie_video", service.get_movie_video, 78)
test("get_tv_115", service.get_tv_pan115, 1396)
test("get_tv_season_magnet", service.get_tv_season_magnet, 1396, 1)
test("get_tv_episode_magnet", service.get_tv_episode_magnet, 1396, 1, 1)
test("get_tv_episode_ed2k", service.get_tv_episode_ed2k, 1396, 1, 1)
test("get_tv_episode_video", service.get_tv_episode_video, 1396, 1, 1)
test("get_person_115", service.get_person_115, 57607)
test("get_collection_pan115", service.get_collection_pan115, 295)

print("\n--- USER Interfaces ---")
test("get_user_info", service.get_user_info)
test("redeem_code", service.redeem_code, "TEST")

print("\n" + "=" * 50)
print("Summary")
print("=" * 50)

ok_count = sum(1 for _, status, _ in results if status == "OK")
fail_count = sum(1 for _, status, _ in results if status == "FAIL")

print(f"OK: {ok_count}")
print(f"FAIL: {fail_count}")

print("\nFailed interfaces:")
for name, status, error in results:
    if status == "FAIL":
        err_msg = error
        if "403" in error:
            err_msg = "403 Forbidden"
        elif "401" in error:
            err_msg = "401 Unauthorized"
        elif "404" in error:
            err_msg = "404 Not Found"
        elif "Cloudflare" in error:
            err_msg = "Cloudflare Blocked"
        print(f"  - {name}: {err_msg}")
