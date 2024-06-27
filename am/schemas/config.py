""""""

from functools import lru_cache

from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(find_dotenv(".env"))


class SchemaSettings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    # special_chars: list[str] # = ["*", "?", ";", "{", "}", "[", "]", "|", "\\", "`", "'", '"', ":"]
    path_delim: str

    default_name: str
    name_min_length: int
    name_max_length: int

    default_description: str
    description_min_length: int
    description_max_length: int

    clientid_min_length: int
    clientid_max_length: int


@lru_cache
def get_schema_settings():
    return SchemaSettings()


if __name__ == "__main__":
    pass
