from dataclasses import dataclass

from koreanbots.domain.abc import KoreanbotsEntity


@dataclass(frozen=True)
class AbstractUser(KoreanbotsEntity):
    """
    FIELD	TYPE	DESCRIPTION
    id	string	유저의 ID
    username	string	유저의 디스코드 사용자 이름
    tag	string	유저의 디스코드 태그
    github	?string	깃허브 닉네임
    flags	integer	유저의 플래그
    bots	Bot[]	소유한 봇들 (단, 소유자는 아이디만 표시됩니다)
    servers	Server[]	소유한 서버들
    """

    id: str
    username: str
    tag: str
    github: str | None
    flags: int
