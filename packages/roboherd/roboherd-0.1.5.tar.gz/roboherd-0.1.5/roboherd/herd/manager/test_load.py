from roboherd.cow import RoboCow

from .load import load_cow


def test_load_cow():
    cow = load_cow("roboherd.examples.moocow", "moocow")
    assert isinstance(cow, RoboCow)


def test_load_cow_can_overwrite_variables():
    one = load_cow("roboherd.examples.moocow", "moocow")

    one.information.name = "A cow eating watermelons"

    two = load_cow("roboherd.examples.moocow", "moocow")

    assert two.information.name == "The mooing cow 🐮"
    assert one.information.name == "A cow eating watermelons"
