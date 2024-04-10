from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    SECRET_AUTH: str
    SECRET_USER_MANAGER: str


    @property
    def SECRET_keys(self):
        return {'auth_key': self.SECRET_AUTH,
                'user_manager_key': self.SECRET_USER_MANAGER
                }

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    model_config = SettingsConfigDict(env_file=".env")

    @property
    def get_db_keys(self):
        return {
            "DB_HOST": self.DB_HOST,
            "DB_PORT": str(self.DB_PORT),
            "DB_USER": self.DB_USER,
            "DB_PASS": self.DB_PASS,
            "DB_NAME": self.DB_NAME
        }

settings = Settings()