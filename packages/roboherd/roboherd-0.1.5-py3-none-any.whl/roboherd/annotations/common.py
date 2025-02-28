from fast_depends import Depends
from typing import Annotated

from roboherd.cow import RoboCow


def get_profile(cow: RoboCow) -> dict:
    if cow.internals.profile is None:
        raise ValueError("Cow has no profile")
    return cow.internals.profile


Profile = Annotated[dict, Depends(get_profile)]
"""The profile of the cow"""
