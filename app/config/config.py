from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mercadopago_token: str
    mongo_db: str

    model_config = SettingsConfigDict(env_file=".env")