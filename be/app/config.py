from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    """应用配置"""

    # OpenAI 配置
    openai_api_key: str
    openai_model: str
    openai_api_base: str

    # MongoDB 配置
    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_db_name: str = "phone_recommend"

    # 服务器配置
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True

    # 日志配置
    log_level: str = "DEBUG"

    # CORS 配置
    cors_origins: List[str] = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "allow"


settings = Settings()  # type: ignore[call-arg]
