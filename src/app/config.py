from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

load_dotenv(".env")


class Settings(BaseSettings):
    mongodb_uri: str
    mongodb_db: str
    s3_endpoint_url: str
    s3_access_key: str
    s3_secret_key: str
    s3_bucket: str

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "forbid",
        "case_sensitive": False,
    }


settings = Settings()  # type: ignore[call-arg]
