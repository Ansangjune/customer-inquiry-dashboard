"""Custom exception classes."""

from fastapi import HTTPException


class ServiceException(HTTPException):
    """Base exception for service-level errors. Subclass for specific cases."""
