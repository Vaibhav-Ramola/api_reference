# this file contains all the required environment variable settings
# that are required on a machine to run the server

from pydantic import BaseSettings


class Settings(BaseSettings):
    # contains all the environment variable that must be configured
    # so this pydantic model checks if all the path variables are available
    # or not with their specified datatype
    # pydantic is not case sensitive 
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    # Default values can be provided but are usually not provided

    class Config:
        env_file = '.env'


settings = Settings()