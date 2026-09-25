from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    app_name: str = "Enterprise AI Assistant"

    version: str = "0.1.0"

    environment: str = "development"

    groq_api_key: str


    model_config = SettingsConfigDict(
        env_file=".env"
    )


settings = Settings()