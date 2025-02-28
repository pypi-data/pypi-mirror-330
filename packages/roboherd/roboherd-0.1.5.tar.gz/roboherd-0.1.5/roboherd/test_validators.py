from dynaconf import Dynaconf

from .validators import validators


def test_validators():
    settings = Dynaconf(validators=validators)

    assert settings.base_url is None
    assert settings.connection_string is None
