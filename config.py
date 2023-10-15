from pydantic_settings import BaseSettings
from typing import List


class ServerConfig(BaseSettings):
    server_host: str
    server_port: int
    server_origins: List[str] = ["*"]
    server_reload: bool = True

    class Config:
        env_file = ".server.env"


class DatabaseConfig(BaseSettings):
    database_host: str
    database_username: str
    database_password: str
    database_port: int
    database_name: str

    class Config:
        env_file = ".db.env"


server_config = ServerConfig()
database_config = DatabaseConfig()
