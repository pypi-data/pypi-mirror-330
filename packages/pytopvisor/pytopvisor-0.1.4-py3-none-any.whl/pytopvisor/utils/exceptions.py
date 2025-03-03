class TopvisorAPIError(Exception):
    """Base exception for Topvisor API."""
    pass


class AuthenticationError(TopvisorAPIError):
    """Exception for authentication errors."""
    pass


class RateLimitError(TopvisorAPIError):
    """Exception for rate limit errors."""
    pass


class InvalidRequestError(TopvisorAPIError):
    """Exception for request validation errors."""
    pass


class ServerError(TopvisorAPIError):
    """Exception for server errors."""
    pass


ERROR_MAPPING = {
    429: RateLimitError,
    503: ServerError,
    53: AuthenticationError,
    54: InvalidRequestError,
    1000: InvalidRequestError,
    1001: InvalidRequestError,
    1002: InvalidRequestError,
    1003: InvalidRequestError,
    1004: InvalidRequestError,
    2000: InvalidRequestError,
    2001: InvalidRequestError,
    2002: InvalidRequestError,
    2003: InvalidRequestError,
    2004: InvalidRequestError,
    2005: InvalidRequestError,
}
