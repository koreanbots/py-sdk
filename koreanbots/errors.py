from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .typing import ErrorMapping


class KoreanbotsExeption(Exception):
    pass


class AuthorizeError(KoreanbotsExeption):
    pass


class HTTPException(KoreanbotsExeption):
    def __init__(self, code, message):
        self.status = code
        if isinstance(message, dict):
            self.status = message.get("code", self.status)
            self.error = message.get("message", "KoreanbotsExeption")
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


ERROR_MAPPING: "ErrorMapping" = {
    400: BadRequest,
    403: Forbidden,
    404: NotFound,
}
