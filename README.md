<div align="center">
  <h1>koreanbots py-sdk</h1>
    
  [![pypi](https://img.shields.io/pypi/v/koreanbots.svg)](https://pypi.org/project/koreanbots/)
  [![pypi](https://img.shields.io/pypi/pyversions/koreanbots.svg)](https://pypi.org/project/koreanbots/)
  [![license](https://img.shields.io/github/license/koreanbots/py-sdk.svg)](https://github.com/koreanbots/py-sdk/blob/master/LICENSE)
  [![downloads](https://img.shields.io/pypi/dm/koreanbots.svg)](https://pypi.org/project/koreanbots/)
  [![codecov](https://codecov.io/gh/koreanbots/py-sdk/branch/master/graph/badge.svg?token=EEZDCQRLW5)](https://codecov.io/gh/koreanbots/py-sdk)
</div>
 
> Official Python SDK for [KOREANBOTS](https://koreanbots.dev)

## 문서

[문서](https://koreanbots.readthedocs.io/en/latest/)

## 예제

discord.py의 `tasks`를 이용해 서버 수를 1시간마다 자동으로 업데이트하는 예제입니다.

```python
import discord
from discord.ext import commands, tasks

from koreanbots import Koreanbots

BOT_TOKEN = "your_discord_bot_token"
KOREANBOTS_API_KEY = "your_koreanbots_api_key"

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())
koreanbots = Koreanbots(KOREANBOTS_API_KEY)


@tasks.loop(hours=1)
async def update_server_count():
    await koreanbots.update_bot_info(
        bot_id=bot.user.id,
        servers=len(bot.guilds),
        shards=bot.shard_count or 0,
    )


@update_server_count.before_loop
async def before_update_server_count():
    await bot.wait_until_ready()


@bot.event
async def on_ready():
    update_server_count.start()
    print(f"Logged in as {bot.user}")


bot.run(BOT_TOKEN)
```
