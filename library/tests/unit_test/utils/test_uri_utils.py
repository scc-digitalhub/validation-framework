from urllib.parse import ParseResult

from datajudge.utils.uri_utils import (
    build_key,
    check_url,
    get_name_from_uri,
    get_uri_netloc,
    get_uri_path,
    get_uri_scheme,
    parse_uri,
    rebuild_uri,
)


class TestURIUtils:
    def test_parse_uri(self) -> None:
        parsed = parse_uri("./test")
        assert isinstance(parsed, ParseResult)

    def test_get_uri_scheme(self) -> None:
        parsed = get_uri_scheme("http://test")
        assert parsed == "http"

    def test_get_uri_netloc(self) -> None:
        parsed = get_uri_netloc("s3://test")
        assert parsed == "test"

    def test_get_uri_path(self) -> None:
        parsed = get_uri_path("s3://test/path/test.csv")
        assert parsed == "/path/test.csv"
        parsed = get_uri_path("test/path/test.csv")
        assert parsed == "test/path/test.csv"

    def test_get_name_from_uri(self) -> None:
        parsed = get_name_from_uri("s3://test/path/test.csv")
        assert parsed == "test.csv"

    def test_rebuild_uri(self) -> None:
        uri = rebuild_uri("http://test.com:5000", "/test")
        assert uri == "http://test.com:5000/test"
        uri = rebuild_uri("file://test", "/test")
        assert uri == "file://test/test"

    def test_build_key(self) -> None:
        uri = build_key("s3://test/5000/test.csv")
        assert uri == "5000/test.csv"

    def test_check_url(self) -> None:
        uri = check_url("http://test.com:5000//test//test")
        assert uri == "http://test.com:5000/test/test"
