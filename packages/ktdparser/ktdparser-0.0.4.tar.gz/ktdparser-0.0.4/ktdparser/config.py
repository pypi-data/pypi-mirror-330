import os


class Settings:
    """KTDParser settings"""
    PROJECT_NAME = "ktdparser"
    PROJECT_VERSION = "0.0.4"
    README = "README.md"
    DESCRIPTION = "PDF parser for special forms using Tabula."

    # Default db settings
    DB_NAME = "ktdparser"
    DB_USER = "ktd_user"
    DB_HOST = "localhost"
    DB_PORT = 5432

    @property
    def log_path(self):
        return os.path.join(os.path.dirname(__file__), "ktdparser.log")


settings = Settings()
