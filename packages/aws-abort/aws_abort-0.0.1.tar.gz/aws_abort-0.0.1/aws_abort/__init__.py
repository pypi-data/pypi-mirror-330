import logging

log = logging.getLogger('abort')


class AbortException(Exception):
    """
    Exception raised for specific HTTP error status codes.

    Attributes:
        status_code (int): The HTTP status code.
        message (str): The error message.
    """

    base_400 = (
        "Bad request, check your code is right, required fields entered?"
    )
    base_401 = (
        "Unauthorized, You Shall Not Pass!"
    )
    base_403 = (
        "Forbidden!"
    )
    base_404 = (
        "Not found, we searched, and we searched, but nothing was there... Sorry."
    )
    base_405 = (
        "Method not allowed, you are not able todo that."
    )
    base_409 = (
        "Pesky constraints! Your request could not be completed due to a constraint, "
        "valid business reason, or inconsistent state."
    )
    base_415 = (
        "Unsupported media! Your request could not be completed as the supplied media is not supported."
    )
    base_424 = (
        "Failed dependency, its not your fault, its not our fault, its THEIR fault!"
    )
    base_429 = (
        "Rate limited, woah there cowboy! Slow it down a bit!"
    )
    base_500 = (
        "Internal server error, we have been alerted."
    )

    def __init__(self, status_code, message):
        """
        Initialize the AbortException.

        Args:
            status_code (int): The HTTP status code.
            message (str): The error message.
        """

        self.status_code = status_code
        self.message = message
        super().__init__(self.message)


def abort(status_code, message=""):
    """
    Handle different HTTP error status codes and raise an AbortException with a detailed message.

    Args:
        status_code (int): The HTTP status code.
        message (str, optional): Additional error message details.

    Raises:
        AbortException: Exception raised with a detailed error message based on the status code.
    """

    log.debug(f"User received a {status_code} error {message}")
    if status_code == 400:
        message = f"{AbortException.base_400} {message}"
    elif status_code == 401:
        message = f"{AbortException.base_401} {message}"
    elif status_code == 403:
        message = f"{AbortException.base_403} {message}"
    elif status_code == 404:
        message = f"{AbortException.base_404} {message}"
    elif status_code == 405:
        message = f"{AbortException.base_405} {message}"
    elif status_code == 409:
        message = f"{AbortException.base_409} {message}"
    elif status_code == 415:
        message = f"{AbortException.base_415} {message}"
    elif status_code == 424:
        log.critical(f"User got a 424 status {message}")
        message = f"{AbortException.base_424} {message}"
    elif status_code == 429:
        log.warning(f"User got a 429 status {message}")
        message = f"{AbortException.base_429} {message}"
    elif status_code == 500:
        log.critical(f"User got a 500 status {message}")
        message = f"{AbortException.base_500} {message}"
    raise AbortException(status_code, message)


# That's all folks...
