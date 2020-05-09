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
    def __init__(self, response):
        self.response = response

    def __getattr__(self, attr):
        return self.response.get(attr)


class userVoted(DBKRResponse):
    def __init__(self, response):
        super().__init__(response)


class Bot(DBKRResponse):
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

Libararies = Enum('Libararies', 
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