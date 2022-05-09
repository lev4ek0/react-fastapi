import os
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    TOKEN: str = os.getenv('BOT_TOKEN')
    WEBHOOK_HOST: str = os.getenv('WEBHOOK_HOST')
    SECRET: str = TOKEN.replace(':', '')
    WEBHOOK_PATH: str = f'/webhook/{SECRET}'
    WEBHOOK_URL: str = f'{WEBHOOK_HOST}/api/bot{WEBHOOK_PATH}'


@lru_cache
def get_config():
    return Settings()
