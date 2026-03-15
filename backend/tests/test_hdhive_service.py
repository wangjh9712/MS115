import asyncio

from app.services.hdhive_service import HDHiveService


class TestHDHiveService:
    def test_extract_current_user_with_points(self) -> None:
        raw = (
            'xxx\\"currentUser\\":{\\"username\\":\\"alice\\",\\"nickname\\":\\"Alice\\",'
            '\\"is_vip\\":true,\\"points\\":128,\\"permissions\\":[]}yyy'
        )

        user = HDHiveService._extract_current_user(raw)

        assert user == {
            "username": "alice",
            "nickname": "Alice",
            "is_vip": True,
            "points": 128,
        }

    def test_extract_current_user_with_credit_balance_text(self) -> None:
        raw = (
            'xxx"currentUser":{"username":"bob","nickname":"","is_vip":0,'
            '"credit_balance":"86 points","permissions":[]}yyy'
        )

        user = HDHiveService._extract_current_user(raw)

        assert user == {
            "username": "bob",
            "nickname": "",
            "is_vip": False,
            "points": 86,
        }

    def test_extract_current_user_with_nested_user_meta_points(self) -> None:
        raw = (
            'xxx"currentUser":{"username":"carol","nickname":"Carol","is_vip":true,'
            '"user_meta":{"points":781,"signin_days_total":37},"permissions":null}yyy'
        )

        user = HDHiveService._extract_current_user(raw)

        assert user == {
            "username": "carol",
            "nickname": "Carol",
            "is_vip": True,
            "points": 781,
        }

    def test_get_user_info_merges_points_from_settings_page(self) -> None:
        service = HDHiveService()

        async def fake_fetch_text(path: str) -> str:
            if path == "/user/settings":
                return (
                    'xxx"currentUser":{"username":"dave","nickname":"Dave","is_vip":true,'
                    '"user_meta":{"points":502},"permissions":null}yyy'
                )
            if path == "/":
                return (
                    'xxx"currentUser":{"username":"dave","nickname":"Dave","is_vip":true,'
                    '"permissions":[]}yyy'
                )
            return ""

        service._fetch_text = fake_fetch_text  # type: ignore[method-assign]

        user = asyncio.run(service.get_user_info())

        assert user == {
            "username": "dave",
            "nickname": "Dave",
            "is_vip": True,
            "points": 502,
        }

    def test_extract_unlock_action_id_from_chunk(self) -> None:
        raw = (
            'xxx(0,e.createServerReference)("40104633e124c17495f8f0497d9a91bd9a5b843744",'
            'e.callServer,void 0,e.findSourceMapURL,"unlockResource")yyy'
        )

        action_id = HDHiveService._extract_unlock_action_id_from_chunk(raw)

        assert action_id == "40104633e124c17495f8f0497d9a91bd9a5b843744"

    def test_extract_next_static_chunk_paths(self) -> None:
        raw = (
            'a "/_next/static/chunks/abc123.js" b '
            '"/_next/static/chunks/def456.js" c '
            '"/_next/static/chunks/abc123.js"'
        )

        paths = HDHiveService._extract_next_static_chunk_paths(raw)

        assert paths == [
            "/_next/static/chunks/abc123.js",
            "/_next/static/chunks/def456.js",
        ]

    def test_resolve_unlock_action_id_ignores_uncached_fallback_id(self) -> None:
        service = HDHiveService()
        service._unlock_action_id = "40dbca7ab6f555dbd98c40945c8b970185c58e16d3"
        service._unlock_action_id_cached_at = 0.0

        async def fake_fetch_text(path: str, accept: str | None = None) -> str:
            assert path == "/_next/static/chunks/runtime.js"
            return (
                '(0,e.createServerReference)("40104633e124c17495f8f0497d9a91bd9a5b843744",'
                'e.callServer,void 0,e.findSourceMapURL,"unlockResource")'
            )

        service._fetch_text = fake_fetch_text  # type: ignore[method-assign]

        action_id = asyncio.run(
            service._resolve_unlock_action_id('"/_next/static/chunks/runtime.js"')
        )

        assert action_id == "40104633e124c17495f8f0497d9a91bd9a5b843744"
