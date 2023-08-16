import pytest

from datajudge.metadata.env_log import EnvLog


@pytest.fixture()
def env():
    return EnvLog()


class TestEnvLog:
    def test_platform(self, env):
        assert isinstance(env.platform, str)

    def test_python_version(self, env):
        assert isinstance(env.python_version, str)

    def test_cpu_model(self, env):
        assert isinstance(env.cpu_model, str)

    def test_cpu_core(self, env):
        assert isinstance(env.cpu_core, int)
        assert env.cpu_core >= 1

    def test_round_ram(self, env):
        assert isinstance(env.round_ram(), str)

    def test_to_dict(self, env):
        assert isinstance(env.to_dict(), dict)

    def test_repr(self, env):
        assert isinstance(repr(env), str)
