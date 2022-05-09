import os
from typing import List, Type

from pydantic import BaseSettings


class Settings(BaseSettings):
    CONFIG_NAME: str = "base"
    USE_MOCK_EQUIVALENCY: bool = False
    DEBUG: bool = False
    TOKEN: str = os.getenv('BOT_TOKEN')
    WEBHOOK_HOST: str = os.getenv('WEBHOOK_HOST')
    SECRET: str = os.getenv('SECRET')
    WEBHOOK_PATH: str = f'/webhook/{SECRET}'
    WEBHOOK_URL: str = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'


class DevelopmentConfig(Settings):
    CONFIG_NAME: str = "dev"
    SECRET_KEY: str = os.getenv("DEV_SECRET_KEY")
    DEBUG: bool = True
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    TESTING: bool = False


class ProductionConfig(Settings):
    CONFIG_NAME: str = "prod"
    SECRET_KEY: str = os.getenv("PROD_SECRET_KEY")
    DEBUG: bool = False
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    TESTING: bool = False


def get_config(config):
    return config_by_name[config]


EXPORT_CONFIGS: List[Type[Settings]] = [
    DevelopmentConfig,
    ProductionConfig,
]
config_by_name = {cfg().CONFIG_NAME: cfg() for cfg in EXPORT_CONFIGS}
