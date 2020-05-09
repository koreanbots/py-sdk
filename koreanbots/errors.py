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
    """koreanbots의 기본 예외 클래스입니다.
    즉, 이 라이브러리의 모든 예외는 이 예외로 잡을 수 있습니다.
    """
    pass

class AuthorizeError(DBKRException):
    """:class:`.Client` 혹은 :class:`.HTTPClient`에게 토큰이 주어지지 않았을떄,
    토큰이 필요한 엔드포인트에 접근하면 발생합니다.
    """
    pass

class HTTPException(DBKRException):
    """:class:`.HTTPClient`의 기본 예외 클래스입니다.
    즉 :class:`.HTTPClient`의 모든 예외는 이 예외로 잡을 수 있습니다.
    """
    def __init__(self, response, message):
        self.status = response.status
        if isinstance(message, dict):
            self.status = message.get('code', self.status)
            self.error = message.get('message', 'DBKRException')
        else:
            self.error = message
        super().__init__(f"{self.status} {self.error}")


class BadRequest(HTTPException):
    """잘못된 파라미터의 리퀘스트입니다.
    파라미터를 확인해주세요.
    """
    pass


class Unauthorized(HTTPException):
    """잘못된 KoreanBots 토큰을 사용했을 떄 발생합니다.
    """
    pass


class Forbidden(HTTPException):
    """접근 권한이 없을 때 발생합니다.
    """
    pass


class NotFound(HTTPException):
    """해당 항목을 찾을 수 없을 때 발생합니다.
    """
    pass