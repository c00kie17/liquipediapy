

class RequestsException(Exception):

    def __init__(self, message, code=500):
        super(RequestsException, self).__init__(message)
        self.code = code
