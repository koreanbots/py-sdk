.. currentmodule:: koreanbots

API 레퍼런스
======================

버전 정보
------------------
.. data:: version_info
    sys.version_info와 비슷한 튜플입니다.

.. data:: __version__
    버전정보의 문자열입니다.

Client
-------

.. autoclass:: Koreanbots
    :members:

Integrations
------------

.. autoclass:: koreanbots.integrations.discord.DiscordpyKoreanbots
    :members:

.. autoclass:: koreanbots.integrations.dico.DicoKoreanbots
    :members:

HTTP
-------------------

.. autoclass:: KoreanbotsRequester
    :members:

Model
-------------------

.. autoclass:: KoreanbotsBot()
    :members:

.. autoclass:: KoreanbotsServer()
    :members:

.. autoclass:: KoreanbotsUser()
    :members:

예외
-------------

.. autoexception:: KoreanbotsException

.. autoexception:: AuthorizeError

.. autoexception:: HTTPException

.. autoexception:: BadRequest

.. autoexception:: Forbidden

.. autoexception:: NotFound
