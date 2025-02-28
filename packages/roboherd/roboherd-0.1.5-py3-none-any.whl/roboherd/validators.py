from dynaconf import Validator

validators = [
    Validator("base_url", default=None),
    Validator("connection_string", default=None),
]
