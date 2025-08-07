"""Custom exception classes for the API."""

import logging
from typing import Any, Dict, Optional

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class APIError(HTTPException):
    """Base API error class."""

    status_code: int = status.HTTP_400_BAD_REQUEST
    error_code: str = "API_ERROR"
    message: str = "An error occurred"

    def __init__(
        self,
        message: Optional[str] = None,
        status_code: Optional[int] = None,
        error_code: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> None:
        self.message = message or self.message
        self.status_code = status_code or self.status_code
        self.error_code = error_code or self.error_code

        detail = {"error_code": self.error_code, "message": self.message, **kwargs}

        super().__init__(
            status_code=self.status_code,
            detail=detail,
            headers=headers,
        )


class ValidationError(APIError):
    """Validation error."""

    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    error_code = "VALIDATION_ERROR"
    message = "Validation failed"


class NotFoundError(APIError):
    """Resource not found error."""

    status_code = status.HTTP_404_NOT_FOUND
    error_code = "NOT_FOUND"
    message = "Resource not found"


class UnauthorizedError(APIError):
    """Unauthorized access error."""

    status_code = status.HTTP_401_UNAUTHORIZED
    error_code = "UNAUTHORIZED"
    message = "Unauthorized access"


class ForbiddenError(APIError):
    """Forbidden access error."""

    status_code = status.HTTP_403_FORBIDDEN
    error_code = "FORBIDDEN"
    message = "Access forbidden"


class ConflictError(APIError):
    """Resource conflict error."""

    status_code = status.HTTP_409_CONFLICT
    error_code = "CONFLICT"
    message = "Resource conflict"


class InternalServerError(APIError):
    """Internal server error."""

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_code = "INTERNAL_SERVER_ERROR"
    message = "Internal server error"


# Legacy errors for backward compatibility
class InvalidToken(UnauthorizedError):
    """Invalid token error."""

    error_code = "INVALID_TOKEN"
    message = "Invalid or expired token"


class ModelProviderNotFound(NotFoundError):
    """Model provider not found error."""

    error_code = "MODEL_PROVIDER_NOT_FOUND"
    message = "Model provider not found"


class ModelNotFound(NotFoundError):
    """Model not found error."""

    error_code = "MODEL_NOT_FOUND"
    message = "Model not found"


async def api_error_handler(request: Request, exc: APIError) -> JSONResponse:
    """Global API error handler."""
    logger.error(
        f"API Error: {exc.error_code} - {exc.message}",
        extra={"request_url": str(request.url), "error_code": exc.error_code},
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
        headers=exc.headers,
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Global HTTP exception handler."""
    logger.error(
        f"HTTP Exception: {exc.status_code} - {exc.detail}",
        extra={"request_url": str(request.url)},
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_code": "HTTP_EXCEPTION",
            "message": (
                exc.detail if isinstance(exc.detail, str) else "HTTP error occurred"
            ),
            "status_code": exc.status_code,
        },
        headers=getattr(exc, "headers", None),
    )
