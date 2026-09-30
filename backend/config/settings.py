from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    APP_NAME: str = "Enterprise Knowledge Assistant"

    ENVIRONMENT: str = "development"

    GROQ_API_KEY: str

    MODEL_NAME: str = "openai/gpt-oss-20b"

    VECTORSTORE_PATH: str = "vectorstore/chroma_db"

    DOCUMENT_PATH: str = "data/documents"

    MAX_FILE_SIZE_MB: int = 20


    BACKEND_HOST: str = "127.0.0.1"

    BACKEND_PORT: int = 8000

    JWT_SECRET_KEY: str

    JWT_ALGORITHM: str = "HS256"
    
    JWT_EXPIRE_MINUTES: int = 60


    model_config = SettingsConfigDict(
        env_file=".env"
    )


settings = Settings()