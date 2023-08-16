import re

from datajudge.utils.utils import flatten_list, get_time, listify, get_uiid


class TestUtils:
    def test_get_uiid(self) -> None:
        assert len(get_uiid()) == 32
        assert get_uiid("test") == "test"

    def test_flatten_list(self):
        list_ = flatten_list([[1], [1, 1], [1]])
        assert list_ == [1, 1, 1, 1]
        assert not flatten_list([1, [1, 1], [1]])
        list_ = flatten_list(
            [
                [1],
            ]
        )
        assert list_ == [1]

    def test_listify(self):
        assert isinstance(listify(1), list)
        assert isinstance(listify([1]), list)
        assert isinstance(listify([{"test": 1}]), list)

    def test_get_time(self) -> None:
        date = get_time()
        # Excpected format
        # 2022-03-14T09:40:12.387+01:00
        regex = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}\+\d{2}:\d{2}$"
        assert bool(re.match(regex, date))
