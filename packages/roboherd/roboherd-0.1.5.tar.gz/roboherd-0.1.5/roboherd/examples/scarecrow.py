from roboherd.cow import RoboCow
from roboherd.cow.types import Information

from roboherd.annotations import PublishObject
from roboherd.annotations.bovine import ObjectFactory

from .meta import meta_information

bot = RoboCow(
    information=Information(
        name="The scare crow 👩‍🌾",
        description="""On startup I scare crows""",
        handle="scarecrow",
        meta_information=meta_information,
    )
)


@bot.startup
async def startup(publish_object: PublishObject, object_factory: ObjectFactory):
    note = object_factory.note(content="Booo! 🐦").as_public().build()  # type: ignore
    await publish_object(note)
