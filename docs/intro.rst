.. currentmodule:: koreanbots

소개
==================

요구사항
------------------------
koreanbots는 파이썬 3.6+에 호환됩니다.
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
    import koreanbots

    client = discord.Client()
    Bot = koreanbots.Client(client, 'KoreanBots 토큰')

    @client.event
    async def on_ready():
        print(f'{client.user}로 로그인하였습니다.')

    client.run('Discord 토큰')

아이디로 봇 정보 가져오기
~~~~~~~~~~~~~~~~~~~~~~~~~

discord.py 사용시

.. code:: py

    import discord
    import koreanbots

    client = discord.Client()
    Bot = koreanbots.Client(client, 'KoreanBots 토큰')

    @client.event
    async def on_ready():
        print(f'{client.user}로 로그인하였습니다.')

        Data = await Bot.getBot('653534001742741552')
        # 반환되는 데이터는 옆 링크를 참고해주세요: https://koreanbots.cf/js-sdk/interfaces/_types_.getbyid.html

        print(Data)

    client.run('Discord 토큰')

discord.py 미사용시

.. code:: py

    import koreanbots

    Bot = koreanbots.HTTPClient('KoreanBots 토큰')
    # getBot은 토큰이 필요하지 않기에 'KoreanBots 토큰' 부분은 생략 가능합니다.

    Data = loop.run_until_complete(Bot.getBot('653534001742741552'))
    # 반환되는 데이터는 옆 링크를 참고해주세요: https://koreanbots.cf/js-sdk/interfaces/_types_.getbyid.html

    print(Data)
