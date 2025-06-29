from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_URL: str 
    JWT_SECRET:str
    JWT_ALGORITHM:str
    REFRESH_TOKEN_EXPIRY_DAYS: int
    REDIS_URL: str
    REDIS_HOST:str
    REDIS_PORT: int

    class Config:
        env_file = ".env"  
        extra = "forbid" 

settings = Settings()
