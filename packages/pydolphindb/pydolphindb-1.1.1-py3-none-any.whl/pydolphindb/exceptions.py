class Error(Exception):

    def __init__(self, msg=None, error_trace=None):
        # for compatibility reasons we want to keep the exception message
        # attribute because clients may depend on it
        if msg:
            self.message = msg
        super(Error, self).__init__(msg)
        self.error_trace = error_trace


class Warning(Exception):
    pass


class InterfaceError(Error):
    pass


class DatabaseError(Error):
    pass


class InternalError(DatabaseError):
    pass


class OperationalError(DatabaseError):
    pass


class ProgrammingError(DatabaseError):
    pass


class IntegrityError(DatabaseError):
    pass


class DataError(DatabaseError):
    pass


class NotSupportedError(DatabaseError):
    pass


# exceptions not in db api
class ConnectionError(OperationalError):
    pass


class BlobException(Exception):
    pass


class DigestNotFoundException(BlobException):
    pass


class BlobLocationNotFoundException(BlobException):
    pass


class TimezoneUnawareException(Error):
    pass
