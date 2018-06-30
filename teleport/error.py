class TeleportException(Exception):
    """Base class for all Teleport exceptions"""


class DataException(TeleportException):
    """Represents an error condition related to input data"""

