"""
Nullbr API 接口配置
定义所有 API 端点的元数据，包括路径、参数、鉴权方式等
"""

from typing import Literal

# 鉴权类型
AuthType = Literal["app_id", "app_id+api_key", "none"]

# API 接口配置
# path: URL 路径模板，支持 {param} 格式的路径参数
# method: HTTP 方法
# auth: 鉴权方式

API_CONFIG = {
    # ========== META 接口 (仅需 APP_ID) ==========
    "search": {
        "path": "/search",
        "method": "GET",
        "auth": "app_id",
        "query_params": ["query", "page"],
    },
    "get_list": {
        "path": "/list/{listid}",
        "method": "GET",
        "auth": "app_id",
        "path_params": ["listid"],
        "query_params": ["page"],
    },
    "get_movie": {
        "path": "/movie/{tmdbid}",
        "method": "GET",
        "auth": "app_id",
        "path_params": ["tmdbid"],
    },
    "get_tv": {
        "path": "/tv/{tmdbid}",
        "method": "GET",
        "auth": "app_id",
        "path_params": ["tmdbid"],
    },
    "get_tv_season": {
        "path": "/tv/{tmdbid}/season/{season_number}",
        "method": "GET",
        "auth": "app_id",
        "path_params": ["tmdbid", "season_number"],
    },
    "get_tv_episode": {
        "path": "/tv/{tmdbid}/season/{season_number}/episode/{episode_number}",
        "method": "GET",
        "auth": "app_id",
        "path_params": ["tmdbid", "season_number", "episode_number"],
    },
    "get_person": {
        "path": "/person/{tmdbid}",
        "method": "GET",
        "auth": "app_id",
        "path_params": ["tmdbid"],
        "query_params": ["page"],
    },
    "get_collection": {
        "path": "/collection/{tmdbid}",
        "method": "GET",
        "auth": "app_id",
        "path_params": ["tmdbid"],
    },

    # ========== RES 接口 (需要 APP_ID + API_KEY) ==========
    "get_movie_115": {
        "path": "/movie/{tmdbid}/115",
        "method": "GET",
        "auth": "app_id+api_key",
        "path_params": ["tmdbid"],
    },
    "get_movie_magnet": {
        "path": "/movie/{tmdbid}/magnet",
        "method": "GET",
        "auth": "app_id+api_key",
        "path_params": ["tmdbid"],
    },
    "get_movie_ed2k": {
        "path": "/movie/{tmdbid}/ed2k",
        "method": "GET",
        "auth": "app_id+api_key",
        "path_params": ["tmdbid"],
    },
    "get_movie_video": {
        "path": "/movie/{tmdbid}/video",
        "method": "GET",
        "auth": "app_id+api_key",
        "path_params": ["tmdbid"],
    },
    "get_tv_115": {
        "path": "/tv/{tmdbid}/115",
        "method": "GET",
        "auth": "app_id+api_key",
        "path_params": ["tmdbid"],
    },
    "get_tv_season_magnet": {
        "path": "/tv/{tmdbid}/season/{season_number}/magnet",
        "method": "GET",
        "auth": "app_id+api_key",
        "path_params": ["tmdbid", "season_number"],
    },
    "get_tv_episode_magnet": {
        "path": "/tv/{tmdbid}/season/{season_number}/episode/{episode_number}/magnet",
        "method": "GET",
        "auth": "app_id+api_key",
        "path_params": ["tmdbid", "season_number", "episode_number"],
    },
    "get_tv_episode_ed2k": {
        "path": "/tv/{tmdbid}/season/{season_number}/episode/{episode_number}/ed2k",
        "method": "GET",
        "auth": "app_id+api_key",
        "path_params": ["tmdbid", "season_number", "episode_number"],
    },
    "get_tv_episode_video": {
        "path": "/tv/{tmdbid}/season/{season_number}/episode/{episode_number}/video",
        "method": "GET",
        "auth": "app_id+api_key",
        "path_params": ["tmdbid", "season_number", "episode_number"],
    },
    "get_person_115": {
        "path": "/person/{tmdbid}/115",
        "method": "GET",
        "auth": "app_id+api_key",
        "path_params": ["tmdbid"],
    },
    "get_collection_115": {
        "path": "/collection/{tmdbid}/115",
        "method": "GET",
        "auth": "app_id+api_key",
        "path_params": ["tmdbid"],
    },

    # ========== USER 接口 ==========
    "get_user_info": {
        "path": "/user/info",
        "method": "GET",
        "auth": "app_id+api_key",
    },
    "redeem_code": {
        "path": "/user/redeem",
        "method": "POST",
        "auth": "app_id+api_key",
        "body_params": ["code"],
    },
}
