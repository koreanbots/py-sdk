class DPKRException(Exception):
    pass


class HTTPException(DPKRException):
    def __init__(self, response, message):
        self.status = response.status
        if isinstance(message, dict):
            self.status = message.get('code', self.status)
            self.error = message.get('message', 'DPKRException')
        else:
            self.error = message
        super().__init__(f"{self.status} {self.error}")


class BadRequest(HTTPException):
    pass


class Unauthorized(HTTPException):
    pass


class Forbidden(HTTPException):
    pass


class NotFound(HTTPException):
    pass