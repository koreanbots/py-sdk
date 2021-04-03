"""
MIT License

Copyright (c) 2020 매리

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


class DBKRException(Exception):
    pass


class AuthorizeError(DBKRException):
    pass


class HTTPException(DBKRException):
    def __init__(self, code, message):
        self.status = code
        if isinstance(message, dict):
            self.status = message.get("code", self.status)
            self.error = message.get("message", "DBKRException")
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


error_mapping = {400: BadRequest, 403: Forbidden, 404: NotFound}
