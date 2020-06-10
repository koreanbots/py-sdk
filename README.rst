koreanbots
==========

.. image:: https://img.shields.io/pypi/v/koreanbots.svg
    :target: https://pypi.org/project/koreanbots/
    :alt: PyPI
.. image:: https://img.shields.io/pypi/pyversions/koreanbots.svg
    :target: https://pypi.org/project/koreanbots/
    :alt: PyPI - Python Version
.. image:: https://img.shields.io/github/license/koreanbots/py-sdk.svg
    :target: https://github.com/koreanbots/py-sdk/
    :alt: GitHub
.. image:: https://img.shields.io/pypi/dm/koreanbots.svg
    :target: https://pypi.org/project/koreanbots/
    :alt: PyPI - Downloads

A Simple Python API wrapper for KoreanBots.

문서
-------------

`문서 <https://koreanbots.readthedocs.io/>`_

설치
-------------

**파이썬 3.6 혹은 그 이상이 필요합니다.**

.. code:: sh

    python3 -m pip install koreanbots

예시
-------------

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
        # 반환되는 데이터는 옆 링크를 참고해주세요: https://koreanbots.dev/js-sdk/interfaces/_types_.getbyid.html

        print(Data)

    client.run('Discord 토큰')

discord.py 미사용시

.. code:: py

    import koreanbots
    import asyncio

    loop = asyncio.get_event_loop()

    Bot = koreanbots.HTTPClient('KoreanBots 토큰')
    # getBot은 토큰이 필요하지 않기에 'KoreanBots 토큰' 부분은 생략 가능합니다.

    Data = loop.run_until_complete(Bot.getBot('653534001742741552'))
    # 반환되는 데이터는 옆 링크를 참고해주세요: https://koreanbots.dev/js-sdk/interfaces/_types_.getbyid.html

    print(Data)
