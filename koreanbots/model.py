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