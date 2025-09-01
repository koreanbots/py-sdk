from koreanbots.domain.bot import AbstractBot, BotWithOwnerID
from koreanbots.domain.server import AbstractServer, ServerWithOwnerID
from koreanbots.domain.user import AbstractUser


class User(AbstractUser):
    bots: list[BotWithOwnerID]
    servers: list[ServerWithOwnerID]


class Server(AbstractServer):
    owners: User


class Bot(AbstractBot):
    owners: list[User]
