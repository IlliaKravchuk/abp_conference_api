from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "ABP Conference Booking API"
    # подкл лок докер
    DATABASE_URL: str = "postgresql+psycopg://postgres:password@localhost:5432/conference_db"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()