.. currentmodule:: koreanbots

버전 호환성
==================

3.0.0
------------------

http 요청 메서드 접근 불가
~~~~~~~~~~~~~~~~~~
더이상 KoreanbotsRequester의 메서드를 통한 HTTP 요청이 불가능합니다.

요청 메서드 이름 변경
~~~~~~~~~~~~~~~~~~
기존 통일되지 않은 메서드 이름을 모두 변경하였습니다. 기존 메서드 이름은 deprecated로 변경되며, 다음 메이저 릴리즈에서 제거되므로 새 메서드 이름으로 변경해주세요.

.. code:: py

    import koreanbots

    kb = koreanbots.Koreanbots()

    ...

    # Before
    await kb.guildcount(...)
    kb_user = await kb.userinfo(...)
    kb_bot = await kb.botinfo(...)
    kb_server = await kb.serverinfo(...)
    widget = await kb.widget(...)
    voted_bot = await kb.is_voted_bot(...)
    voted_server = await kb.is_voted_server(...)

    # After
    await kb.post_guild_count(...)
    kb_user = await kb.get_user_info(...)
    kb_bot = await kb.get_bot_info(...)
    kb_server = await kb.get_server_info(...)
    widget = await kb.get_widget(...)
    voted_bot = await kb.get_bot_vote(...)
    voted_server = await kb.get_server_vote(...)

모델 구조 변경
~~~~~~~~~~~~~~~~~~
원본 REST API의 응답과 반환되던 응답 모델이 상이한 부분이 있어 혼선을 방지하기 위해 원본 REST API의 응답과 통일하고자 모델을 수정하였습니다.

이제 정보를 가져올 때 data 속성을 참조해야 합니다.

.. code:: py

    # Before
    r = await koreanbots.botinfo(653534001742741552)
    print(r.owners[0].bots)

    # After
    r = await koreanbots.get_bot_info(653534001742741552)
    print(r.data.owners[0].bots)
