"""
SyncService 解析逻辑测试
"""

from app.services.sync_service import SyncService


def test_extract_receive_code_prefers_explicit() -> None:
    code = SyncService._extract_receive_code(
        "https://115.com/s/abcd1234?password=zzzz",
        {"receive_code": "yyyy"},
        "wxyz",
    )
    assert code == "wxyz"


def test_extract_receive_code_from_payload() -> None:
    code = SyncService._extract_receive_code(
        "https://115.com/s/abcd1234",
        {"receive_code": "a1b2"},
        "",
    )
    assert code == "a1b2"


def test_extract_receive_code_from_short_code() -> None:
    code = SyncService._extract_receive_code("abcd1234-1x2y", None, "")
    assert code == "1x2y"


def test_extract_receive_code_from_password_query() -> None:
    code = SyncService._extract_receive_code("https://115.com/s/abcd1234?password=p9q8", None, "")
    assert code == "p9q8"


def test_extract_receive_code_from_urlencoded_password_query() -> None:
    code = SyncService._extract_receive_code("https%3A%2F%2F115.com%2Fs%2Fabcd1234%3Fpwd%3Dk7m3", None, "")
    assert code == "k7m3"


def test_extract_receive_code_from_text_hint() -> None:
    code = SyncService._extract_receive_code("链接 https://115.com/s/abcd1234 提取码: c3d4", None, "")
    assert code == "c3d4"


def test_extract_share_code_from_payload() -> None:
    code = SyncService._extract_share_code("https://115.com/s/zzzz9999", {"share_code": "abcd1234"})
    assert code == "abcd1234"


def test_extract_share_code_from_url() -> None:
    code = SyncService._extract_share_code("https://115.com/s/abcd1234?password=a1b2", None)
    assert code == "abcd1234"
