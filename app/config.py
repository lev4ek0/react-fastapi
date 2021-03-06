import os
from functools import lru_cache
from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    TOKEN: str = os.getenv('BOT_TOKEN')
    WEBHOOK_HOST: str = os.getenv('WEBHOOK_HOST')
    SECRET: str = TOKEN.replace(':', '')
    WEBHOOK_PATH: str = f'/webhook/{SECRET}'
    WEBHOOK_URL: str = f'{WEBHOOK_HOST}{API_V1_STR}/bot{WEBHOOK_PATH}'


@lru_cache
def get_config():
    return Settings()
