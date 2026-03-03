import httpx
from typing import Any, Set, Tuple
from app.core.config import settings

class EmbyService:
    def __init__(self):
        self.base_url = settings.EMBY_URL.rstrip('/')
        self.api_key = settings.EMBY_API_KEY

    def set_config(self, base_url: str, api_key: str) -> None:
        self.base_url = str(base_url or "").strip().rstrip("/")
        self.api_key = str(api_key or "").strip()

    async def get_downloaded_episodes_with_status(self, tmdb_id: int) -> dict[str, Any]:
        """
        获取 Emby 中已存在的某个剧集的具体集数
        返回格式:
        {
          "status": "ok|not_configured|request_failed",
          "message": "...",
          "episodes": {(season_num, episode_num), ...}
        }
        """
        if not self.base_url or not self.api_key:
            return {
                "status": "not_configured",
                "message": "Emby 未配置",
                "episodes": set(),
            }

        url = f"{self.base_url}/emby/Items"
        params = {
            "api_key": self.api_key,
            "ProviderIds.Tmdb": tmdb_id,
            "IncludeItemTypes": "Episode",
            "Recursive": "true",
            "Fields": "ProviderIds"
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params, timeout=10.0)
                response.raise_for_status()
                data = response.json()
                
                existing_episodes = set()
                for item in data.get("Items", []):
                    # ParentIndexNumber 通常是季号，IndexNumber 是集号
                    season_num = item.get("ParentIndexNumber")
                    episode_num = item.get("IndexNumber")
                    
                    if episode_num is not None:
                        # Emby中如果是特别篇等，可能没有正常的season，我们默认给季号为1如果缺失
                        season = season_num if season_num is not None else 1
                        existing_episodes.add((int(season), int(episode_num)))
                return {
                    "status": "ok",
                    "message": "查询成功",
                    "episodes": existing_episodes,
                }
            except Exception as e:
                print(f"Error fetching from Emby: {e}")
                return {
                    "status": "request_failed",
                    "message": str(e),
                    "episodes": set(),
                }

    async def get_downloaded_episodes(self, tmdb_id: int) -> Set[Tuple[int, int]]:
        result = await self.get_downloaded_episodes_with_status(tmdb_id)
        return set(result.get("episodes") or set())
    
    async def refresh_library(self):
        """触发 Emby 扫描库更新"""
        if not self.base_url or not self.api_key:
            return
            
        url = f"{self.base_url}/emby/Library/Refresh"
        params = {"api_key": self.api_key}
        
        async with httpx.AsyncClient() as client:
            try:
                # 触发扫描是不返回具体内容的
                await client.post(url, params=params, timeout=5.0)
            except Exception as e:
                print(f"Error triggering Emby refresh: {e}")

    async def check_connection(self) -> dict[str, Any]:
        if not self.base_url or not self.api_key:
            return {
                "valid": False,
                "message": "Emby URL 或 API Key 未配置",
                "user": None,
            }

        url = f"{self.base_url}/emby/System/Info"
        params = {"api_key": self.api_key}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params, timeout=10.0)
                response.raise_for_status()
                payload = response.json() if response.content else {}
                if not isinstance(payload, dict):
                    payload = {}
                return {
                    "valid": True,
                    "message": "Emby 连接成功",
                    "user": {
                        "server_name": payload.get("ServerName"),
                        "version": payload.get("Version"),
                        "id": payload.get("Id"),
                    },
                }
            except Exception as exc:
                return {
                    "valid": False,
                    "message": str(exc),
                    "user": None,
                }

emby_service = EmbyService()
