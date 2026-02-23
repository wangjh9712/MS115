"""
Nullbr 服务层
基于通用客户端，提供与原有接口兼容的服务方法
"""

from typing import Optional
from app.services.nullbr_client import nullbr_client


class NullbrService:
    """Nullbr API 服务类"""

    def __init__(self):
        self.client = nullbr_client

    # ========== META 接口 ==========

    def search(self, query: str, page: int = 1) -> dict:
        """
        搜索电影、电视剧、人物、合集

        Args:
            query: 搜索关键字
            page: 页码，默认 1
        """
        return self.client.search(query=query, page=page)

    def get_list(self, list_id: int, page: int = 1) -> dict:
        """
        获取列表详细信息

        Args:
            list_id: 列表 ID
            page: 页码，默认 1
        """
        return self.client.get_list(listid=list_id, page=page)

    def get_movie(self, tmdb_id: int) -> dict:
        """
        获取电影详细信息

        Args:
            tmdb_id: TMDB ID
        """
        return self.client.get_movie(tmdbid=tmdb_id)

    def get_tv(self, tmdb_id: int) -> dict:
        """
        获取电视剧详细信息

        Args:
            tmdb_id: TMDB ID
        """
        return self.client.get_tv(tmdbid=tmdb_id)

    def get_tv_season(self, tmdb_id: int, season_number: int) -> dict:
        """
        获取电视剧季信息

        Args:
            tmdb_id: TMDB ID
            season_number: 季号
        """
        return self.client.get_tv_season(tmdbid=tmdb_id, season_number=season_number)

    def get_tv_episode(self, tmdb_id: int, season_number: int, episode_number: int) -> dict:
        """
        获取电视剧集信息

        Args:
            tmdb_id: TMDB ID
            season_number: 季号
            episode_number: 集号
        """
        return self.client.get_tv_episode(
            tmdbid=tmdb_id,
            season_number=season_number,
            episode_number=episode_number
        )

    def get_person(self, tmdb_id: int, page: int = 1) -> dict:
        """
        获取人物信息

        Args:
            tmdb_id: TMDB ID
            page: 页码，默认 1
        """
        return self.client.get_person(tmdbid=tmdb_id, page=page)

    def get_collection(self, tmdb_id: int) -> dict:
        """
        获取电影合集信息

        Args:
            tmdb_id: TMDB ID (合集 ID)
        """
        return self.client.get_collection(tmdbid=tmdb_id)

    # ========== RES 接口 (需要 API Key) ==========

    def get_movie_pan115(self, tmdb_id: int, page: int = 1) -> dict:
        """
        获取电影 115 网盘资源

        Args:
            tmdb_id: TMDB ID
            page: 页码，默认 1
        """
        result = self.client.get_movie_115(tmdbid=tmdb_id)
        return {
            "id": result.get("id", tmdb_id),
            "media_type": result.get("media_type", "movie"),
            "page": result.get("page", 1),
            "total_page": result.get("total_page", 1),
            "list": result.get("115", []),
        }

    def get_movie_magnet(self, tmdb_id: int) -> dict:
        """
        获取电影磁力资源

        Args:
            tmdb_id: TMDB ID
        """
        result = self.client.get_movie_magnet(tmdbid=tmdb_id)
        return {
            "id": result.get("id", tmdb_id),
            "media_type": result.get("media_type", "movie"),
            "list": result.get("magnet", []),
        }

    def get_movie_ed2k(self, tmdb_id: int) -> dict:
        """
        获取电影 ed2k 资源

        Args:
            tmdb_id: TMDB ID
        """
        result = self.client.get_movie_ed2k(tmdbid=tmdb_id)
        return {
            "id": result.get("id", tmdb_id),
            "media_type": result.get("media_type", "movie"),
            "list": result.get("ed2k", []),
        }

    def get_movie_video(self, tmdb_id: int) -> dict:
        """
        获取电影 m3u8 视频资源

        Args:
            tmdb_id: TMDB ID
        """
        result = self.client.get_movie_video(tmdbid=tmdb_id)
        return {
            "id": result.get("id", tmdb_id),
            "media_type": result.get("media_type", "movie"),
            "list": result.get("video", []),
        }

    def get_tv_pan115(self, tmdb_id: int, page: int = 1) -> dict:
        """
        获取电视剧 115 网盘资源

        Args:
            tmdb_id: TMDB ID
            page: 页码，默认 1
        """
        result = self.client.get_tv_115(tmdbid=tmdb_id)
        return {
            "id": result.get("id", tmdb_id),
            "media_type": result.get("media_type", "tv"),
            "page": result.get("page", 1),
            "total_page": result.get("total_page", 1),
            "list": result.get("115", []),
        }

    def get_tv_season_magnet(self, tmdb_id: int, season_number: int) -> dict:
        """
        获取电视剧季磁力资源

        Args:
            tmdb_id: TMDB ID
            season_number: 季号
        """
        result = self.client.get_tv_season_magnet(
            tmdbid=tmdb_id,
            season_number=season_number
        )
        return {
            "id": result.get("id", tmdb_id),
            "season_number": result.get("season_number", season_number),
            "media_type": result.get("media_type", "tv"),
            "list": result.get("magnet", []),
        }

    def get_tv_episode_magnet(self, tmdb_id: int, season_number: int, episode_number: int) -> dict:
        """
        获取电视剧集磁力资源

        Args:
            tmdb_id: TMDB ID
            season_number: 季号
            episode_number: 集号
        """
        result = self.client.get_tv_episode_magnet(
            tmdbid=tmdb_id,
            season_number=season_number,
            episode_number=episode_number
        )
        return {
            "tv_show_id": result.get("tv_show_id", tmdb_id),
            "season_number": result.get("season_number", season_number),
            "episode_number": result.get("episode_number", episode_number),
            "media_type": result.get("media_type", "tv"),
            "list": result.get("magnet", []),
        }

    def get_tv_episode_ed2k(self, tmdb_id: int, season_number: int, episode_number: int) -> dict:
        """
        获取电视剧集 ed2k 资源

        Args:
            tmdb_id: TMDB ID
            season_number: 季号
            episode_number: 集号
        """
        result = self.client.get_tv_episode_ed2k(
            tmdbid=tmdb_id,
            season_number=season_number,
            episode_number=episode_number
        )
        return {
            "tv_show_id": result.get("tv_show_id", tmdb_id),
            "season_number": result.get("season_number", season_number),
            "episode_number": result.get("episode_number", episode_number),
            "media_type": result.get("media_type", "tv"),
            "list": result.get("ed2k", []),
        }

    def get_tv_episode_video(self, tmdb_id: int, season_number: int, episode_number: int) -> dict:
        """
        获取电视剧集 m3u8 视频资源

        Args:
            tmdb_id: TMDB ID
            season_number: 季号
            episode_number: 集号
        """
        result = self.client.get_tv_episode_video(
            tmdbid=tmdb_id,
            season_number=season_number,
            episode_number=episode_number
        )
        return {
            "tv_show_id": result.get("tv_show_id", tmdb_id),
            "season_number": result.get("season_number", season_number),
            "episode_number": result.get("episode_number", episode_number),
            "media_type": result.get("media_type", "tv"),
            "list": result.get("video", []),
        }

    def get_person_115(self, tmdb_id: int) -> dict:
        """
        获取人物 115 网盘合集

        Args:
            tmdb_id: TMDB ID
        """
        result = self.client.get_person_115(tmdbid=tmdb_id)
        return {
            "id": result.get("id", tmdb_id),
            "media_type": result.get("media_type", "person"),
            "page": result.get("page", 1),
            "total_page": result.get("total_page", 1),
            "list": result.get("115", []),
        }

    def get_collection_pan115(self, tmdb_id: int, page: int = 1) -> dict:
        """
        获取电影合集 115 网盘资源

        Args:
            tmdb_id: TMDB ID (合集 ID)
            page: 页码，默认 1
        """
        result = self.client.get_collection_115(tmdbid=tmdb_id)
        return {
            "id": result.get("id", tmdb_id),
            "media_type": result.get("media_type", "collection"),
            "page": result.get("page", 1),
            "total_page": result.get("total_page", 1),
            "list": result.get("115", []),
        }

    # ========== USER 接口 ==========

    def get_user_info(self) -> dict:
        """
        获取用户订阅信息和配额使用情况
        """
        return self.client.get_user_info()

    def redeem_code(self, code: str) -> dict:
        """
        使用提示码兑换订阅升级

        Args:
            code: 提示码
        """
        return self.client.redeem_code(code=code)

    # ========== 便捷方法 ==========

    def get_tv_magnet(
        self,
        tmdb_id: int,
        season: Optional[int] = None,
        episode: Optional[int] = None
    ) -> dict:
        """
        获取电视剧磁力资源（便捷方法）

        Args:
            tmdb_id: TMDB ID
            season: 季号
            episode: 集号
        """
        if season is not None and episode is not None:
            return self.get_tv_episode_magnet(tmdb_id, season, episode)
        elif season is not None:
            return self.get_tv_season_magnet(tmdb_id, season)
        return self.get_tv_season_magnet(tmdb_id, 1)

    def get_tv_ed2k(
        self,
        tmdb_id: int,
        season: Optional[int] = None,
        episode: Optional[int] = None
    ) -> dict:
        """
        获取电视剧 ed2k 资源（便捷方法）
        """
        if season is not None and episode is not None:
            return self.get_tv_episode_ed2k(tmdb_id, season, episode)
        return self.get_tv_episode_ed2k(tmdb_id, 1, 1)

    def get_tv_video(
        self,
        tmdb_id: int,
        season: Optional[int] = None,
        episode: Optional[int] = None
    ) -> dict:
        """
        获取电视剧 m3u8 视频资源（便捷方法）
        """
        if season is not None and episode is not None:
            return self.get_tv_episode_video(tmdb_id, season, episode)
        return self.get_tv_episode_video(tmdb_id, 1, 1)


# 创建服务实例
nullbr_service = NullbrService()
