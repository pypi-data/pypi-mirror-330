from fast_depends import Depends
from typing import Annotated, Callable, Awaitable

from almabtrieb import Almabtrieb


def get_raw(data: dict) -> dict:
    return data.get("data", {}).get("raw")


def get_parsed(data: dict) -> dict:
    result = data.get("data", {}).get("parsed")
    if result is None:
        raise ValueError("No parsed data found")
    return result


RawData = Annotated[dict, Depends(get_raw)]
"""The raw data as received by cattle_grid"""

ParsedData = Annotated[dict, Depends(get_parsed)]
"""The parsed data as transformed by muck_out"""


def get_activity(parsed: ParsedData) -> dict:
    result = parsed.get("activity")
    if not result:
        raise ValueError("No activity found")
    return result


def get_embedded_object(parsed: ParsedData) -> dict:
    result = parsed.get("embeddedObject")
    if not result:
        raise ValueError("No embedded object found")
    return result


Activity = Annotated[dict, Depends(get_activity)]
"""The activity parsed by muck_out"""

EmbeddedObject = Annotated[dict, Depends(get_embedded_object)]
"""The embedded object in the activity as parsed by muck_out"""

Publisher = Callable[[dict], Awaitable[None]]
"""Type returned by the publishing functions"""


def construct_publish_object(connection: Almabtrieb, actor_id: str) -> Publisher:
    async def publish(data: dict):
        await connection.trigger("publish_object", {"actor": actor_id, "data": data})

    return publish


def construct_publish_activity(connection: Almabtrieb, actor_id: str) -> Publisher:
    async def publish(data: dict):
        await connection.trigger("publish_activity", {"actor": actor_id, "data": data})

    return publish


PublishObject = Annotated[Publisher, Depends(construct_publish_object)]
"""Allows one to publish an object as the actor. Assumes cattle_grid has the extension `simple_object_storage` or equivalent"""


PublishActivity = Annotated[Publisher, Depends(construct_publish_activity)]
"""Allows one to publish an activity as the actor. Assumes cattle_grid has the extension `simple_object_storage` or equivalent"""
