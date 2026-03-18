from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE: int = 20
    ALGORITHM: str = "HS256"
    DB_URL: str


    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = 'allow'
        
settings = Settings()


def get_auth_data():
    return {"secret_key": settings.SECRET_KEY, "algorithm": settings.ALGORITHM}