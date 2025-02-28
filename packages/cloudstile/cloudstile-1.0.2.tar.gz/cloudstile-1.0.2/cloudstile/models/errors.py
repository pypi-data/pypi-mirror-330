class CloudStileError(Exception):
    """Base class for all custom errors"""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class HTTPError(CloudStileError):
    """Error class for HTTP related errors"""

    def __init__(self, status_code: int, message: str):
        super().__init__(message)
        self.status_code = status_code


class InvalidInputSecret(CloudStileError):
    """
    Exception raised for invalid input secret in CloudStile.

    This exception is raised when the provided secret parameter is invalid,
    does not exist, or is a testing secret key that results in a non-testing
    response. It indicates that the input secret does not meet the required
    criteria for successful validation.

    Attributes:
        message (str): An explanation of the error.
    """
