"""
Handles application configuration management by loading environment variables.

This module uses `pydantic-settings` to define, validate, and access all
configuration settings from a `.env` file or from the system's environment.
Centralizing configuration in this way is a best practice for modern applications.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Defines the application's environment variables using Pydantic's BaseSettings.

    Each attribute of this class corresponds to an environment variable that the
    application needs to run. Pydantic automatically reads these variables from
    the environment or a specified .env file and performs type validation.
    """

    database_host: str
    database_port: int
    database_user: str
    database_password: str
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # Pydantic configuration to specify the source of the settings.
    model_config = SettingsConfigDict(env_file=".env")


# Create a single, global instance of the Settings class.
# This instance should be imported into other modules to access configuration values,
# ensuring that settings are loaded only once.
settings = Settings()
