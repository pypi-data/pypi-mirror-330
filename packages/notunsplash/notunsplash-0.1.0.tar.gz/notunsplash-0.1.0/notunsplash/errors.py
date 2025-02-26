"""
Custom exceptions for the Unsplash SDK
"""

class UnsplashError(Exception):
    """Base exception for Unsplash API errors"""
    pass

class UnsplashAuthError(UnsplashError):
    """Exception raised for authentication-related errors"""
    pass
