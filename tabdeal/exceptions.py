class CoreException(Exception):
    pass


class UnStructuredResponseException(CoreException):
    def __init__(self, status, message):
        self.status = status
        self.message = message

    def __str__(self):
        return self.message


class ClientException(CoreException):
    def __init__(self, status, message, code, detail=None):
        self.status = status
        self.message = message
        self.code = code
        self.detail = detail

    def __str__(self):
        return self.message


class ServerException(CoreException):
    def __init__(self, status, message, detail=None):
        self.status = status
        self.message = message
        self.detail = detail

    def __str__(self):
        return self.message


class ParameterRequiredException(CoreException):
    def __init__(self, param, action):
        self.param = param
        self.action = action

    def __str__(self):
        return "'{}' field is required for {}".format(self.param, self.action)


class SecurityException(CoreException):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
