koreanbots
==========

![image](https://img.shields.io/pypi/v/koreanbots.svg%0A%20:target:%20https://pypi.org/project/koreanbots/%0A%20:alt:%20PyPI)

![image](https://img.shields.io/pypi/pyversions/koreanbots.svg%0A%20:target:%20https://pypi.org/project/koreanbots/%0A%20:alt:%20PyPI%20-%20Python%20Version)

![image](https://img.shields.io/github/license/koreanbots/py-sdk.svg%0A%20:target:%20https://github.com/koreanbots/py-sdk/%0A%20:alt:%20GitHub)

![image](https://img.shields.io/pypi/dm/koreanbots.svg%0A%20:target:%20https://pypi.org/project/koreanbots/%0A%20:alt:%20PyPI%20-%20Downloads)

A Python API wrapper for KoreanBots.

설치
----

**파이썬 3.6 혹은 그 이상이 필요합니다.**

```sh
python3 -m pip install koreanbots
```

로거
----

*koreanbots* 는 파이썬의 `logging` 모듈을 사용하여 로깅합니다.

간단한 디버깅을 위해 `INFO` 이상의 로깅을 추천합니다.

### `logging` 설정 예시

```python
import logging

logger = logging.getLogger('koreanbots')
logger.setLevel(logging.INFO) # DEBUG INFO WARNING ERROR CRITICAL
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('[%(asctime)s] [%(filename)s] [%(name)s:%(module)s] [%(levelname)s]: %(message)s'))
logger.addHandler(handler)
```

예시
----

**개발중입니다**