import os
from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    TOKEN: str = os.getenv('BOT_TOKEN')
    WEBHOOK_HOST: str = os.getenv('WEBHOOK_HOST')
    SECRET: str = os.getenv('SECRET')
    WEBHOOK_PATH: str = f'/webhook/{SECRET}'
    WEBHOOK_URL: str = f'{WEBHOOK_HOST}/api/bot{WEBHOOK_PATH}'


def get_config():
    return Settings()
