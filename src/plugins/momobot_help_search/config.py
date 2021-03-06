from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    json_path = "/home/zfj/workspeace/zfjdhj.github.io/zfjbot-helpWebsite/data.json"

    class Config:
        extra = "ignore"