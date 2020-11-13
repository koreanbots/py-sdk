from typing import Union


class KoreanBotsException(Exception):
    pass


class AuthorizeError(KoreanBotsException):
    pass


class RequestFailedError(KoreanBotsException):
    pass


class HTTPException(KoreanBotsException):
    def __init__(self, response, message: Union[str, dict]) -> None:
        self.status: int = response.status

        if isinstance(message, dict):
            self.status: int = message.get("code", self.status)
            self.error: str = message.get("message", "KoreanBotsException")
        else:
            self.error: str = message

        super().__init__(f"{self.status} {self.error}")


class BadRequest(HTTPException):
    pass


class Unauthorized(HTTPException):
    pass


class Forbidden(HTTPException):
    pass


class NotFound(HTTPException):
    pass


class GraphQLError(KoreanBotsException):
    pass