from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    appid = "xxxxxxxx"  # 填写你的appid
    secretKey = "xxxxxxxxx"  # 填写你的密钥

    class Config:
        extra = "ignore"