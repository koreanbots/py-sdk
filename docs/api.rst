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

.. autoclass:: Client
    :members:

HTTPClient
-------------------

.. autoclass:: HTTPClient
    :members:

Enumerations
-------------

.. autoclass:: Category
    :members:

.. autoclass:: Library
    :members:

예외
-------------

.. autoexception:: DBKRException

.. autoexception:: AuthorizeError

.. autoexception:: HTTPException

.. autoexception:: BadRequest

.. autoexception:: Unauthorized

.. autoexception:: Forbidden

.. autoexception:: NotFound