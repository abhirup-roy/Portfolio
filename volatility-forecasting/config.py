import os 
from pydantic_settings import BaseSettings


def return_full_path(filename: str = ".env") -> str:
    abs_path = os.path.abspath(__file__)
    dir_path = os.path.dirname(abs_path)
    full_path = os.path.join(dir_path, filename)
    return full_path

class Settings(BaseSettings):
    alpha_api_key: str
    db_name: str
    model_directory: str
    
    class Config:
        env_file = return_full_path(".env")

settings = Settings()