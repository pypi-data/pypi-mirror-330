from dataclasses import dataclass, field

from roboherd.cow import RoboCow
from .load import load_cow


@dataclass
class CowConfig:
    name: str = field(metadata={"description": "Name of the cow, must be unique"})
    module: str
    attribute: str
    config: dict

    @staticmethod
    def from_name_and_dict(name, cow: dict) -> "CowConfig":
        module, attribute = cow["bot"].split(":")

        return CowConfig(name=name, module=module, attribute=attribute, config=cow)

    def load(self) -> RoboCow:
        cow = load_cow(self.module, self.attribute)

        if "name" in self.config:
            cow.information.name = self.config["name"]
        if "handle" in self.config:
            cow.information.handle = self.config["handle"]

        if "base_url" in self.config:
            cow.internals.base_url = self.config["base_url"]

        return cow

    def __hash__(self):
        return hash(self.name)


@dataclass
class HerdConfig:
    cows: list[CowConfig] = field(default_factory=list)

    def for_name(self, name: str) -> CowConfig | None:
        for cow in self.cows:
            if cow.name == name:
                return cow
        return None

    @property
    def names(self) -> set[str]:
        return {cow.name for cow in self.cows}

    @staticmethod
    def from_settings(settings):
        cows = [
            CowConfig.from_name_and_dict(name, config)
            for name, config in settings.cow.items()
        ]

        return HerdConfig(cows=cows)

    def load_herd(self) -> list[RoboCow]:
        return [cow.load() for cow in self.cows]
