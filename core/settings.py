
from typing import Optional, Union
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):

    APP_TITLE: str = Field(default='UniQuad')


    SECRET_KEY: str = Field(default=...)
    ALGORITHM: str = Field(default='HS256')

    DATABASE_URL: str = Field(default="sqlite:///./test.db")

    TIMEZONE: str = Field(default='Africa/Nairobi')

    ELASTICSEARCH_URL: Optional[str] = Field(default=None)
    ELASTICSEARCH_API_KEY: Union[str, None] = Field(default=None)
    BROKER_URL: Optional[str]  = Field(default=None)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        case_sensitive=True,
        extra="ignore"
    )



settings = Settings()


