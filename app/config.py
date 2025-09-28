from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_DRIVER: str = "psycopg2"

    @property
    def sqlalchemy_database_url(self) -> str:
        return f"postgresql+{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = "/home/wesley/Projects/FASTapi/app/.env"
        env_file_encoding = 'utf-8'

settings = Settings()