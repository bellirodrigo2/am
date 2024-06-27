""""""

from functools import lru_cache

from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(find_dotenv(".env"))

# # # # # # # # # # # # # # # # # # #
# ler sobre mais opções...........
# https://docs.pydantic.dev/latest/concepts/pydantic_settings/#validation-of-default-values
# # # # # # # # # # # # # # # # # # #


class FieldLabelSetting(BaseSettings):

    default_name: str
    name_min_length: int
    name_max_length: int

    default_description: str
    description_min_length: int
    description_max_length: int

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8", env_prefix="fieldlabel_"
    )


class SQLAlchemySettings(BaseSettings):
    database_url: str
    test_database_url: str

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8", env_prefix="sqlalchemy_"
    )


@lru_cache
def get_sqlalchemy_settings():
    return SQLAlchemySettings()


@lru_cache
def get_fieldrules_setting():
    return FieldLabelSetting()


if __name__ == "__main__":
    print(get_fieldrules_setting())
    print(get_sqlalchemy_settings())
