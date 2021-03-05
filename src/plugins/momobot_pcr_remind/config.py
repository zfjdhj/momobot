from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    bot_id = "1475166415"

    class Config:
        extra = "ignore"