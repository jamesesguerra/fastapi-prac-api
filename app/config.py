from pydantic import BaseSettings

# validates that env variables are set
class Settings(BaseSettings):
    # provide list of env variables that we need to set
    db_url: str
    secret_key: str
    algorithm: str
    access_token_exp_mins: int

    class Config:
        env_file = '.env'

settings = Settings()