from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "N100 Financial Intelligence API"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = True
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    WORKERS: int = 1

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
