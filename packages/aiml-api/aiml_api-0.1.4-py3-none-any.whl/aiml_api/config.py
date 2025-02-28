from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    aiml_api_url: str
    aiml_api_key: str
    model_config = SettingsConfigDict(env_file=".env", envenv_prefix="AIML_API")


settings = Settings()
