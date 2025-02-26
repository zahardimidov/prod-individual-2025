import logging
from os import getenv


class BaseSettings:
    def __init__(self):
        for k, v in self.__annotations__.items():
            env_value = getenv(k)
            default_value = getattr(self.__class__, k, None)
            if env_value is None:
                setattr(self, k, default_value)
            else:
                setattr(self, k, v(env_value))


class Settings(BaseSettings):
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    MINIO_URL: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int

    ENGINE: str
    TEST_MODE: int = 0

settings = Settings()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)