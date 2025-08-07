import os
from functools import lru_cache
from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    # Application Configuration
    PROJECT_NAME: str = Field(
        default="AI WorkFlow",
        description="The name of the project",
    )
    VERSION: str = Field(default="0.1.0", description="Application version")
    API_PREFIX: str = Field(default="/api/v1", description="API prefix path")
    DEBUG: bool = Field(default=False, description="Debug mode")

    # Environment
    ENVIRONMENT: str = Field(
        default="development",
        description="Environment (development, staging, production)",
    )
    IS_LOCAL: bool = Field(default=True, description="Whether running locally")

    # Database Configuration
    DATABASE_URI: str = Field(
        default="sqlite+aiosqlite:///app.db",
        description="Database connection URI",
    )
    ECHO_SQL: bool = Field(default=False, description="Echo SQL queries")

    # Security
    SECRET_KEY: str = Field(
        default="dev-secret-key-change-in-production",
        description="Secret key for cryptographic operations",
    )

    # External Services
    SENTRY_DSN: Optional[str] = Field(
        default=None, description="Sentry DSN for error tracking"
    )

    # CORS Configuration
    ALLOWED_ORIGINS: list[str] = Field(
        default=["*"], description="Allowed CORS origins"
    )

    # Server Configuration
    HOST: str = Field(default="0.0.0.0", description="Server host")
    PORT: int = Field(default=8001, description="Server port")
    WORKERS: int = Field(default=1, description="Number of worker processes")

    # Logging
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")

    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Validate environment values."""
        allowed = ["development", "staging", "production"]
        if v not in allowed:
            raise ValueError(f"Environment must be one of {allowed}")
        return v

    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level values."""
        allowed = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in allowed:
            raise ValueError(f"Log level must be one of {allowed}")
        return v.upper()

    @field_validator("DATABASE_URI")
    @classmethod
    def validate_database_uri(cls, v: str) -> str:
        """Validate database URI format."""
        if not v:
            raise ValueError("Database URI cannot be empty")
        return v

    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.ENVIRONMENT == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.ENVIRONMENT == "development"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        validate_assignment = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Global settings instance
settings = get_settings()
