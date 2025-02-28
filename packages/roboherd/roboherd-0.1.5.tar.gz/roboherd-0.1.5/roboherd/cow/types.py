from pydantic import BaseModel, Field

from .const import default_icon


class MetaInformation(BaseModel):
    """Meta Information about the bot. This includes
    information such as the author and the source repository"""

    source: str | None = Field(
        default=None,
        examples=["https://forge.example/repo"],
        description="The source repository",
    )

    author: str | None = Field(
        default=None,
        examples=["acct:author@domain.example"],
        description="The author, often a Fediverse handle",
    )


class Information(BaseModel):
    """Information about the cow"""

    type: str = Field(
        default="Service",
        examples=["Service"],
        description="ActivityPub type of the actor.",
    )

    handle: str | None = Field(
        default=None,
        examples=["moocow"],
        description="Used as the handle in `acct:handle@domain.example`",
    )

    name: str | None = Field(
        default=None,
        examples=["The mooing cow 🐮"],
        description="The display name of the cow",
    )

    description: str | None = Field(
        default=None,
        examples=[
            "I'm a cow that moos.",
            """<p>An example bot to illustrate Roboherd</p><p>For more information on RoboHerd, see <a href="https://codeberg.org/bovine/roboherd">its repository</a>.</p>""",
        ],
        description="The description of the cow, used as summary of the actor",
    )

    icon: dict = Field(
        default=default_icon,
        description="The profile image",
    )

    frequency: str | None = Field(
        default=None,
        examples=["daily"],
        description="Frequency of posting. Is set automatically if cron expressions are used.",
    )

    meta_information: MetaInformation = Field(
        default=MetaInformation(),
        description="Meta information about the cow, such as the source repository",
    )
