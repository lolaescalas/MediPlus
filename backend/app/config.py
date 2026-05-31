from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # MongoDB Atlas
    mongo_uri: str
    mongo_db_name: str

    # Neo4j Aura
    neo4j_uri: str
    neo4j_user: str
    neo4j_password: str

    # API
    api_host: str = "localhost"
    api_port: int = 8000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


# Instancia global — importar desde otros módulos:
#   from app.config import settings
settings = Settings()
