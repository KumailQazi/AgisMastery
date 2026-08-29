from pydantic_settings import BaseSettings

class SettingsWithArmor(BaseSettings):
    APP_ENV: str = "development"
    SECRET_KEY: str = "change-me-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    DATABASE_URL: str = "sqlite:///./mastery.db"
    REDIS_URL: str = "redis://localhost:6379/0"
    GEMINI_API_KEY: str = ""
    GOOGLE_CLOUD_PROJECT_ID: str = ""
    GOOGLE_CLOUD_LOCATION: str = "us-central1"
    USE_FIRESTORE: bool = False
    
    # Model Armor Configuration
    MODEL_ARMOR_ENABLED: bool = True
    MODEL_ARMOR_TEMPLATE_ID: str = "mastery-pii-template"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings_with_armor = SettingsWithArmor()
