import pytest

from .types import Information, MetaInformation
from .const import default_icon
from .profile import determine_profile_update


@pytest.mark.parametrize(
    "info_params, profile",
    [
        ({}, {"type": "Service"}),
        ({"name": "name"}, {"type": "Service", "name": "name"}),
        ({"description": "description"}, {"type": "Service", "summary": "description"}),
    ],
)
def test_determine_profile_update_no_update(info_params, profile):
    profile["icon"] = default_icon
    info = Information(**info_params)

    assert determine_profile_update(info, profile) is None


def test_determine_profile_update():
    info = Information(name="name", description="description")
    profile = {"id": "http://host.test/actor/1"}

    result = determine_profile_update(info, profile)

    assert result == {
        "actor": "http://host.test/actor/1",
        "profile": {
            "type": "Service",
            "name": "name",
            "summary": "description",
            "icon": default_icon,
        },
    }


def test_determine_profile_update_author():
    info = Information(meta_information=MetaInformation(author="acct:author@host.test"))
    profile = {
        "id": "http://host.test/actor/1",
        "type": "Service",
        "icon": default_icon,
    }

    result = determine_profile_update(info, profile)

    assert result == {
        "actor": "http://host.test/actor/1",
        "actions": [
            {
                "action": "update_property_value",
                "key": "Author",
                "value": "acct:author@host.test",
            }
        ],
    }


def test_profile_update_for_new_preferredUsername():
    info = Information(handle="handle")
    profile = {
        "id": "http://host.test/actor/1",
        "type": "Service",
        "icon": default_icon,
    }

    result = determine_profile_update(info, profile)

    assert result == {
        "actor": "http://host.test/actor/1",
        "actions": [
            {
                "action": "add_identifier",
                "identifier": "acct:handle@host.test",
                "primary": True,
            }
        ],
    }
