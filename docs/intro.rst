.. currentmodule:: koreanbots

소개
==================

요구사항
------------------------
koreanbots는 파이썬 3.8+에 호환됩니다.
discord.py와 함께 사용이 가능하지만 필수는 아닙니다.

설치
---------------
.. code:: sh

    python3 -m pip install koreanbots

빠른 시작
----------------------

서버수 업데이트하기
~~~~~~~~~~~~~~~~~~~~~~~~~

주기적으로 봇의 수를 업데이트합니다. (discord.py)

.. code:: py

    import discord
    from koreanbots.integrations.discord import DiscordpyKoreanbots

    client = discord.Client()
    kb = DiscordpyKoreanbots(client, 'KoreanBots 토큰', run_task=True)

    @client.event
    async def on_ready():
        print(f'{client.user}로 로그인하였습니다.')

    client.run('Discord 토큰')

아이디로 봇 정보 가져오기
~~~~~~~~~~~~~~~~~~~~~~~~~

discord.py 사용시

.. code:: py

    import discord
    from koreanbots.integrations.discord import DiscordpyKoreanbots

    client = discord.Client()
    kb = DiscordpyKoreanbots(client, 'KoreanBots 토큰', run_task=True)

    @client.event
    async def on_ready():
        print(f'{client.user}로 로그인하였습니다.')

        data = await kb.botinfo('653534001742741552')

        print(data.name)

    client.run('Discord 토큰')

discord.py 미사용시

.. code:: py

    import koreanbots

    kb = koreanbots.Koreanbots()

    data = loop.run_until_complete(kb.botinfo('653534001742741552'))

    print(data.name)
