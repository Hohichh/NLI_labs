from dataclasses import dataclass
from environs import Env

@dataclass
class TgBot:
    token: str

@dataclass
class Config:
    tg_Bot: TgBot

def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_Bot=TgBot(token=env('BOT_TOKEN')))