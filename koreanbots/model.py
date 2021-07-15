from typing import Any, Dict, List, Optional, Union

from .abc import KoreanbotsABC
from .typing import Category, State, Status


class BaseKoreanbots(KoreanbotsABC):
    def __init__(self, **response_data: Any) -> None:
        self._response_data = response_data

    @property
    def code(self) -> int:
        """
        상태 코드를 반환합니다.

        :return:
            상태 코드
        :rtype:
            int
        """
        return self._response_data.get("code", 0)

    @property
    def version(self) -> int:
        """
        버전을 반환합니다.

        :return:
            버전
        :rtype:
            int
        """
        return self._response_data.get("version", 0)

    @property
    def data(self) -> Dict[str, Any]:
        """
        데이터를 반환합니다.

        :return:
            데이터 딕셔너리
        :rtype:
            Dict(str, Any)
        """
        return self._response_data.get("data", {})


class KoreanbotsBot(BaseKoreanbots):
    """
    봇의 정보를 가져왔을떄 반환되는 인스턴스입니다.

    :param init_in_user:
        유저 클래스에서 초기화 되었는지 여부입니다. 기본값은 False입니다.
    :type init_in_user: bool

    """

    def __init__(
        self,
        init_in_user: bool = False,
        **response_data: Any,
    ) -> None:
        super().__init__(**response_data)
        self.init_in_user = init_in_user

    @property
    def id(self) -> Optional[str]:
        """
        아이디를 반환합니다.

        :return:
            아이디

        :rtype:
            Optional[str]
        """
        return self.data.get("id")

    @property
    def name(self) -> Optional[str]:
        """
        이름을 반환합니다.

        :return:
            이름
        :rtype:
            Optional[str]
        """
        return self.data.get("name")

    @property
    def tag(self) -> Optional[str]:
        """
        태그를 반환합니다.

        :return:
            태그
        :rtype:
            Optional[str]
        """
        return self.data.get("tag")

    @property
    def avatar(self) -> Optional[str]:
        """
        아바타를 반환합니다.


        :return:
            아바타 url
        :rtype:
            Optional[str]
        """
        return self.data.get("avatar")

    @property
    def owners(self) -> Union[List["KoreanbotsUser"], List[str]]:
        """
        소유자를 반환합니다.
        ※ init_in_user가 True인경우 소유자들의 ID를 반환합니다.

        :return:
            소유자들의 ID들을 담고 있는 리스트 또는 KoreanbotsUser 인스턴스를 담고있는 리스트
        :rtype:
            Union[List[str], List[KoreanbotsUser]]

        """
        if self.init_in_user:
            return self._response_data.get("owners", [])

        return list(
            map(
                lambda user: KoreanbotsUser(True, **user),
                self.data.get("owners", []),
            )
        )

    @property
    def flags(self) -> int:
        """
        플래그를 반환합니다.

        :return:
            플래그
        :rtype:
            int
        """
        return self.data.get("flags", 0)

    @property
    def lib(self) -> Optional[str]:
        """
        봇이 사용한 라이브러리를 반환합니다.

        :return:
            라이브러리
        :rtype:
            Optional[str]
        """
        return self.data.get("lib")

    @property
    def prefix(self) -> Optional[str]:
        """
        프리픽스를 반환합니다.

        :return:
            프리픽스
        :rtype:
            Optional[str]
        """
        return self.data.get("prefix")

    @property
    def votes(self) -> int:
        """
        투표수를 반환합니다.

        :return:
            투표수
        :rtype:
            int
        """
        return self.data.get("votes", 0)

    @property
    def servers(self) -> int:
        """
        서버수를 반환합니다.

        :return:
            서버수
        :rtype:
            int
        """
        return self.data.get("servers", 0)

    @property
    def shards(self) -> int:
        """
        샤드수를 반환합니다.

        :return:
            샤드수
        :rtype:
            int
        """
        return self.data.get("shards", 0)

    @property
    def intro(self) -> Optional[str]:
        """
        소개문구를 반환합니다.

        :return:
            소개문구
        :rtype:
            Optional[str]
        """
        return self.data.get("intro")

    @property
    def desc(self) -> Optional[str]:
        """
        설명문구를 반환합니다.

        :return:
            설명문구
        :rtype:
            Optional[str]
        """
        return self.data.get("desc")

    @property
    def web(self) -> Optional[str]:
        """
        웹사이트 주소를 반환합니다.

        :return:
            웹사이트 주소
        :rtype:
            Optional[str]
        """
        return self.data.get("web")

    @property
    def git(self) -> Optional[str]:
        """
        깃 주소를 반환합니다.

        :return:
            깃 주소
        :rtype:
            Optional[str]
        """
        return self.data.get("git")

    @property
    def url(self) -> Optional[str]:
        """
        주소를 반환합니다

        :return:
            주소
        :rtype:
            Optional[str]
        """
        return self.data.get("url")

    @property
    def discord(self) -> Optional[str]:
        """
        디스코드 주소를 반환합니다.

        :return:
            디스코드 주소
        :rtype:
            Optional[str]
        """
        return self.data.get("discord")

    @property
    def category(self) -> Optional[Category]:
        """
        카테고리를 반환합니다.

        :return:
            카테고리
        :rtype:
            Optional[Category]
        """
        return self.data.get("category")

    @property
    def vanity(self) -> Optional[str]:
        """
        봇의 가상 주소를 반환합니다.

        :return:
            봇의 가상 주소
        :rtype:
            Optional[str]
        """
        return self.data.get("vanity")

    @property
    def bg(self) -> Optional[str]:
        """
        배경 이미지 주소를 반환합니다.

        :return:
            배경 이미지 주소
        :rtype:
            Optional[str]
        """
        return self.data.get("bg")

    @property
    def banner(self) -> Optional[str]:
        """
        배너 이미지 주소를 반환합니다.

        :return:
            배너 이미지 주소
        :rtype:
            Optional[str]
        """
        return self.data.get("banner")

    @property
    def status(self) -> Optional[Status]:
        """
        상태를 반환합니다.

        :return:
            상태
        :rtype:
            Optional[Status]
        """
        return self.data.get("status")

    @property
    def state(self) -> Optional[State]:
        """
        Koreanbots에서의 상태를 반환합니다.

        :return:
            Koreanbots에서의 상태
        :rtype:
            Optional[State]
        """
        return self.data.get("state")


class KoreanbotsUser(BaseKoreanbots):
    """
    유저 정보를 가져왔을때 반환되는 클래스입니다.

    :param init_in_bot:
        봇 클래스에서 초기화 되었는지 여부입니다. 기본값은 False입니다.
    :type init_in_bot: bool

    """

    def __init__(self, init_in_bot: bool = False, **response_data: Any) -> None:
        super().__init__(**response_data)
        self.init_in_bot = init_in_bot

    @property
    def id(self) -> int:
        """
        ID를 반환합니다.

        :return:
            ID
        :rtype:
            int
        """
        return self.data.get("id", 0)

    @property
    def username(self) -> str:
        """
        유저 이름을 반환합니다.

        :return:
            유저 이름
        :rtype:
            str
        """
        return self.data.get("username", "")

    @property
    def tag(self) -> str:
        """
        태그를 반환합니다.

        :return:
            태그
        :rtype:
            str
        """
        return self.data.get("tag", "")

    @property
    def github(self) -> Optional[str]:
        """
        GitHub 주소를 반환합니다.

        :return:
            GitHub 주소
        :rtype:
            Optional[str]
        """
        return self.data.get("github", None)

    @property
    def flags(self) -> int:
        """
        플래그를 반환합니다.

        :return:
            플래그
        :rtype:
            int
        """
        return self.data.get("flags", 0)

    @property
    def bots(
        self,
    ) -> Union[List[KoreanbotsBot], List[str]]:
        """
        봇들을 반환합니다.
        ※ init_in_bot가 True인경우 봇들의 ID를 반환합니다.

        :return:
            봇들의 ID들을 담고 있는 리스트 또는 KoreanbotsUser 인스턴스를 담고있는 리스트
        :rtype:
            Union[List[str], List[KoreanbotsUser]]

        """
        if self.init_in_bot:
            return self._response_data.get("bots", [])

        return list(
            map(
                lambda bot: KoreanbotsBot(True, **bot),
                self.data.get("bots", []),
            )
        )


class KoreanbotsVote(BaseKoreanbots):
    def __init__(self, **response_data: Any) -> None:
        super().__init__(**response_data)

    @property
    def voted(self) -> bool:
        return self.data.get("voted", False)

    @property
    def last_vote(self) -> int:
        return self.data.get("lastVote", 0)
