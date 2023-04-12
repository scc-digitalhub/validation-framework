import pytest
from datajudge.plugins.plugin_factory import builder_factory


class TestBuilderFactory:
    def test_returns_list(self):
        config = []
        typology = ""
        stores = {}
        result = builder_factory(config, typology, stores)
        assert isinstance(result, list)

    def test_raises_not_implemented_error(self):
        config = [{"library": "invalid"}]
        typology = ""
        stores = {}
        with pytest.raises(NotImplementedError):
            builder_factory(config, typology, stores)
