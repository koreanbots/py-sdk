from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union

from .typing import Category, State, Status


@dataclass(eq=False, frozen=True)
class BaseKoreanbots:
    code: int = field(repr=True)  # 상태 코드
    version: int = field(repr=True)  # 버전
    data: Dict[str, Any] = field(repr=False)  # 데이터 딕셔너리


@dataclass(eq=True, frozen=True)
class KoreanbotsBot(BaseKoreanbots):
    """
    봇의 정보를 가져왔을떄 반환되는 인스턴스입니다.
    """

    id: Optional[str] = field(repr=True, compare=True, default=None)  # 아이디
    name: Optional[str] = field(repr=True, compare=False, default=None)  # 이름
    tag: Optional[str] = field(repr=False, compare=False, default=None)  # 태그
    avatar: Optional[str] = field(repr=False, compare=False, default=None)  # 아바타
    flags: int = field(repr=False, compare=False, default=0)  # 플래그
    lib: Optional[str] = field(repr=False, compare=False, default=None)  # 라이브러리
    prefix: Optional[str] = field(repr=False, compare=False, default=None)  # 프리픽스
    votes: int = field(repr=False, compare=False, default=0)  # 투표 수
    servers: int = field(repr=False, compare=False, default=0)  # 서버 수
    shards: int = field(repr=False, compare=False, default=0)  # 샤드 수
    intro: Optional[str] = field(repr=False, compare=False, default=None)  # 소개 문구
    desc: Optional[str] = field(repr=False, compare=False, default=None)  # 설명 문구
    web: Optional[str] = field(repr=False, compare=False, default=None)  # 웹사이트 주소
    git: Optional[str] = field(repr=False, compare=False, default=None)  # 깃 주소
    url: Optional[str] = field(repr=False, compare=False, default=None)  # 주소
    discord: Optional[str] = field(repr=False, compare=False, default=None)  # 디스코드 주소
    category: Optional[Category] = field(
        repr=False, compare=False, default=None
    )  # 카테고리
    vanity: Optional[str] = field(repr=False, compare=False, default=None)  # 가상 주소
    bg: Optional[str] = field(repr=False, compare=False, default=None)  # 배경 이미지 주소
    banner: Optional[str] = field(repr=False, compare=False, default=None)  # 배너 이미지 주소
    status: Optional[Status] = field(repr=False, compare=False, default=None)  # 상태
    state: Optional[State] = field(
        repr=False, compare=False, default=None
    )  # Koreanbots에서의 상태

    _owners: List[str] = field(repr=False, compare=False, default_factory=list)  # 봇들
    init_in_user: bool = field(
        repr=False, compare=False, default=False
    )  # .owners 에서 소유자들의 ID를 반환하는지의 여부

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
            return self._owners

        return list(map(lambda user: KoreanbotsUser(True, **user), self._owners))


@dataclass(eq=True, frozen=True)
class KoreanbotsUser(BaseKoreanbots):
    """
    유저 정보를 가져왔을때 반환되는 클래스입니다.
    """

    id: int = field(repr=True, compare=True, default=0)  # 아이디
    username: str = field(repr=True, compare=False, default="")  # 유저 이름
    tag: str = field(repr=False, compare=False, default="")  # 태그
    github: Optional[str] = field(repr=False, compare=False, default=None)  # Github 주소
    flags: int = field(repr=False, compare=False, default=0)  # 플래그
    _bots: List[str] = field(repr=False, compare=False, default_factory=list)
    init_in_bot: bool = field(
        repr=False, compare=False, default=False
    )  # .bots 에서 봇들의 ID를 반환하는지의 여부

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
            return self._bots

        return list(map(lambda bot: KoreanbotsBot(True, **bot), self._bots))


@dataclass(eq=True, frozen=True)
class Emoji:
    """
    이모지 정보를 가져왔을때 반환되는 클래스입니다.
    """

    id: int = field(repr=True, compare=True, default=0)  # ID
    name: str = field(repr=True, compare=False, default="")  # 이모지 이름
    url: str = field(repr=False, compare=False, default="")  # 이모지 url


@dataclass(eq=True, frozen=True)
class KoreanbotsServer(BaseKoreanbots):
    """
    서버 정보를 가져왔을때 반환되는 클래스입니다.
    """

    id: int = field(repr=True, compare=True, default=0)  # ID
    name: str = field(repr=True, compare=False, default="")  # 서버 이름
    flags: int = field(repr=False, compare=False, default=0)  # 플래그
    intro: Optional[str] = field(repr=False, compare=False, default=None)  # 소개문구
    desc: Optional[str] = field(repr=False, compare=False, default=None)  # 설명문구
    votes: int = field(repr=True, compare=False, default=0)  # 투표수
    category: Optional[Category] = field(
        repr=False, compare=False, default=None
    )  # 카테고리
    invite: str = field(repr=False, compare=False, default="")  # 초대링크
    state: Optional[State] = field(
        repr=False, compare=False, default=None
    )  # Koreanbots에서의 상태
    vanity: Optional[str] = field(repr=False, compare=False, default=None)  # 서버의 가상 주소
    bg: Optional[str] = field(repr=False, compare=False, default=None)  # 배경 이미지 주소
    banner: Optional[str] = field(repr=False, compare=False, default=None)  # 배너 이미지 주소
    icon: Optional[str] = field(repr=False, compare=False, default=None)  # 아이콘
    members: int = field(repr=False, compare=False, default=0)  # 멤버 수
    emojis: List[Emoji] = field(
        repr=False, compare=False, default_factory=list
    )  # Emoji 인스턴스를 담고 있는 리스트
    boostTier: int = field(repr=False, compare=False, default=0)  # 부스트 레벨
    _bots: List[str] = field(repr=False, compare=False, default_factory=list)
    init_in_bot_user: bool = field(
        repr=False, compare=False, default=False
    )  # .bots 에서 봇들의 ID를 반환하는지의 여부

    @property
    def bots(
        self,
    ) -> Union[List[KoreanbotsBot], List[str]]:
        """
        봇들을 반환합니다.
        ※ init_in_bot_user가 True인경우 봇들의 ID를 반환합니다.
        :return:
            봇들의 ID들을 담고 있는 리스트 또는 KoreanbotsUser 인스턴스를 담고있는 리스트
        :rtype:
            Union[List[str], List[KoreanbotsUser]]
        """
        if self.init_in_bot_user:
            return self._bots

        return list(map(lambda bot: KoreanbotsBot(True, **bot), self._bots))


@dataclass(eq=True, frozen=True)
class KoreanbotsVote(BaseKoreanbots):
    voted: bool = field(repr=True, compare=True, default=False)  # 투표 여부
    last_vote: int = field(repr=True, compare=True, default=0)  # 마지막으로 투표한 일자
