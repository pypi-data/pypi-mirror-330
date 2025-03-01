class JestitException(Exception):
    """
    Base exception class for Jestit-related errors.

    Attributes:
        reason (str): The reason for the exception.
        code (int): The error code associated with the exception.
        status (int, optional): The HTTP status code. Defaults to None.
    """

    def __init__(self, reason, code, status=500):
        """
        Initialize a JestitException instance.

        Args:
            reason (str): The reason for the exception.
            code (int): The error code associated with the exception.
            status (int, optional): The HTTP status code. Defaults to None.
        """
        super().__init__(reason)
        self.reason = reason
        self.code = code
        self.status = status

class PermissionDeniedException(JestitException):
    """
    Exception raised for permission denied errors.

    Attributes:
        reason (str): The reason for the exception. Defaults to 'Permission Denied'.
        code (int): The error code associated with the exception. Defaults to 403.
        status (int, optional): The HTTP status code. Defaults to 403.
    """

    def __init__(self, reason='Permission Denied', code=403, status=403):
        """
        Initialize a PermissionDeniedException instance.

        Args:
            reason (str, optional): The reason for the exception. Defaults to 'Permission Denied'.
            code (int, optional): The error code associated with the exception. Defaults to 403.
            status (int, optional): The HTTP status code. Defaults to 403.
        """
        super().__init__(reason, code, status)

class RestErrorException(JestitException):
    """
    Exception raised for REST API errors.

    Attributes:
        reason (str): The reason for the exception. Defaults to 'REST API Error'.
        code (int): The error code associated with the exception. Defaults to 500.
        status (int, optional): The HTTP status code. Defaults to 500.
    """

    def __init__(self, reason='REST API Error', code=500, status=500):
        """
        Initialize a RestErrorException instance.

        Args:
            reason (str, optional): The reason for the exception. Defaults to 'REST API Error'.
            code (int, optional): The error code associated with the exception. Defaults to 500.
            status (int, optional): The HTTP status code. Defaults to 500.
        """
        super().__init__(reason, code, status)
