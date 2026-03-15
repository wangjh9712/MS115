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
