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

class DBKRResponse:
    r""".HTTPClient의 모든 반환 데이터에 대한 기본 모델입니다.

    속성
    -----------
    response: dict
        반환되는 데이터의 dict입니다.
    attribute
        attribute의 이름을 입력하면 해당 값을 반환합니다.
    """
    def __init__(self, response):
        self.response = response

    def __getattr__(self, attr):
        return self.response.get(attr)
    
    def __dict__(self):
        return self.response


class userVoted(DBKRResponse):
    r""".HTTPClient의 유저 하트 정보 데이터의 모델입니다.

    속성
    -----------
    response: dict
        반환되는 데이터의 dict입니다.
    attribute
        attribute의 이름을 입력하면 해당 값을 반환합니다.
    """
    def __init__(self, response):
        super().__init__(response)


class Bot(DBKRResponse):
    r""".HTTPClient의 봇 정보 데이터의 모델입니다.

    속성
    -----------
    response: dict
        반환되는 데이터의 dict입니다.
    attribute
        attribute의 이름을 입력하면 해당 값을 반환합니다.
    """
    def __init__(self, response):
        super().__init__(response)

        
class User(DBKRResponse):
    r""".HTTPClient의 유저 정보 데이터의 모델입니다.

    속성
    -----------
    response: dict
        반환되는 데이터의 dict입니다.
    attribute
        attribute의 이름을 입력하면 해당 값을 반환합니다.
    """
    def __init__(self, response):
        super().__init__(response)

        
from enum import Enum

Category = Enum('Category', 
    [
     '관리',
     '뮤직',
     '전적',
     '웹 대시보드',
     '로깅',
     '도박',
     '게임',
     '밈',
     '레벨링',
     '유틸리티',
     '번역',
     '대화',
     'NSFW',
     '검색'
    ]
)

Library = Enum('Library', 
    [
    'discord.js',
    'Eris',
    'discord.py',
    'discordcr',
    'Nyxx',
    'Discord.Net',
    'DSharpPlus',
    'Nostrum',
    'coxir',
    'DiscordGo',
    'Discord4J',
    'Javacord',
    'JDA',
    'Discordia',
    'RestCord',
    'Yasmin',
    'disco',
    'discordrb',
    'serenity',
    'SwiftDiscord',
    'Sword',
    '기타',
    '비공개'
    ]
)
