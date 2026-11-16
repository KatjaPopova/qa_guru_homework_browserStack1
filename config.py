from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    browserstack_username: str
    browserstack_access_key: str
    browserstack_url: str = "hub.browserstack.com"
    android_app: str = "bs://sample.app"
    ios_app: str = "bs://sample.app"
    project_name: str = "QA Guru Homework"
    build_name: str = "browserstack-build-1"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()