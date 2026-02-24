import asyncio
import base64
import html
import re
from urllib.parse import quote
from urllib.request import Request, urlopen

import httpx


class SeedHubService:
    def __init__(self, base_url: str = "https://www.seedhub.cc") -> None:
        self.base_url = base_url.rstrip("/")
        self._headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/123.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        }

    async def search_magnets_by_keyword(self, keyword: str, limit: int = 40) -> list[dict]:
        normalized_keyword = str(keyword or "").strip()
        if not normalized_keyword:
            return []

        movie_ids = await self._search_movie_ids(normalized_keyword, limit=4)
        if not movie_ids:
            return []

        collected: list[dict] = []
        seen_magnets: set[str] = set()

        for movie_id in movie_ids:
            entries = await self._fetch_seed_entries(movie_id)
            if not entries:
                continue

            semaphore = asyncio.Semaphore(4)

            async def resolve(entry: dict) -> dict | None:
                async with semaphore:
                    magnet = await self._resolve_magnet(entry["seed_id"])
                if not magnet:
                    return None

                magnet_key = magnet.lower()
                if magnet_key in seen_magnets:
                    return None
                seen_magnets.add(magnet_key)
                return {
                    "id": f"seedhub-{entry['seed_id']}",
                    "name": entry["title"] or f"SeedHub 资源 #{entry['seed_id']}",
                    "title": entry["title"] or f"SeedHub 资源 #{entry['seed_id']}",
                    "size": entry["size"],
                    "magnet": magnet,
                    "source_service": "seedhub",
                    "seed_id": entry["seed_id"],
                    "updated_at": entry["updated_at"],
                    "movie_id": movie_id,
                }

            resolved_items = await asyncio.gather(
                *(resolve(entry) for entry in entries),
                return_exceptions=True,
            )
            for item in resolved_items:
                if isinstance(item, dict):
                    collected.append(item)
                if len(collected) >= limit:
                    return collected[:limit]

        return collected[:limit]

    async def _search_movie_ids(self, keyword: str, limit: int = 4) -> list[str]:
        url = f"{self.base_url}/s/{quote(keyword)}/"
        text = await self._fetch_text(url)
        if not text:
            return []

        movie_ids: list[str] = []
        seen: set[str] = set()
        for match in re.findall(r"/movies/(\d+)/", text):
            if match in seen:
                continue
            seen.add(match)
            movie_ids.append(match)
            if len(movie_ids) >= limit:
                break
        return movie_ids

    async def _fetch_seed_entries(self, movie_id: str) -> list[dict]:
        url = f"{self.base_url}/movies/{movie_id}/"
        text = await self._fetch_text(url)
        if not text:
            return []

        entries: list[dict] = []
        seen_ids: set[str] = set()
        pattern = re.compile(
            r"<li>\s*(?P<a><a[^>]+href=\"/link_start/\?seed_id=(?P<seed>\d+)[^\"]*\"[^>]*>.*?</a>)"
            r"\s*/\s*<code class=\"size\">(?P<size>[^<]*)</code>"
            r".*?<span class=\"create-time\"[^>]*>(?P<updated>[^<]*)</span>",
            re.IGNORECASE | re.DOTALL,
        )
        for matched in pattern.finditer(text):
            seed_id = str(matched.group("seed") or "").strip()
            anchor = str(matched.group("a") or "")
            title_match = re.search(r'title="([^"]*)"', anchor, flags=re.IGNORECASE)
            title = title_match.group(1) if title_match else ""
            size = str(matched.group("size") or "").strip()
            updated_at = str(matched.group("updated") or "").strip()
            if seed_id in seen_ids:
                continue
            seen_ids.add(seed_id)
            entries.append(
                {
                    "seed_id": seed_id,
                    "title": html.unescape(str(title or "").strip()),
                    "size": str(size or "").strip(),
                    "updated_at": str(updated_at or "").strip(),
                }
            )
        return entries

    async def _resolve_magnet(self, seed_id: str) -> str:
        url = f"{self.base_url}/link_start/?seed_id={seed_id}&movie_title=seedhub"
        text = await self._fetch_text(url)
        if not text:
            return ""

        matched = re.search(r'const\s+data\s*=\s*"([A-Za-z0-9+/=]+)"', text)
        if not matched:
            return ""

        encoded = matched.group(1)
        try:
            decoded = base64.b64decode(encoded).decode("utf-8", errors="ignore").strip()
        except Exception:
            return ""

        if not decoded.startswith("magnet:?"):
            return ""
        return decoded

    async def _fetch_text(self, url: str) -> str:
        try:
            async with httpx.AsyncClient(
                timeout=20.0,
                follow_redirects=True,
                headers=self._headers,
            ) as client:
                response = await client.get(url)
                response.raise_for_status()
            return response.text
        except Exception:
            return await asyncio.to_thread(self._fetch_text_via_urllib, url)

    def _fetch_text_via_urllib(self, url: str) -> str:
        try:
            req = Request(url, headers=self._headers)
            with urlopen(req, timeout=20) as resp:
                content = resp.read()
            return content.decode("utf-8", errors="ignore")
        except Exception:
            return ""


seedhub_service = SeedHubService()
