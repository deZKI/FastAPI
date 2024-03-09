from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """ Настройки проекта """
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str


    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    SECRET_KEY: str
    ALGORITHM: str
    LOG_LEVEL: int

    class Config:
        env_file = "app/.env"


settings = Settings()
