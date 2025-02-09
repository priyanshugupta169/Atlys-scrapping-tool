from pydantic_settings import BaseSettings

# The class `Settings` defines various configuration settings with default values and an environment
# file `.env`.
class Settings(BaseSettings):
    STATIC_TOKEN: str = "your_static_token_here"
    DEFAULT_PAGE_LIMIT: int = 5
    DEFAULT_PROXY: str = None
    RETRY_DELAY: int = 5
    STORAGE_FILE: str = "data/data.json"
    IMAGE_DIR: str = "data/images"

    class Config:
        env_file = ".env"

settings = Settings()