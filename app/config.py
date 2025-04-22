from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import  Field
import json
from typing import List

class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file="../.env")
    SECRET_KEY: str

settings = Settings()