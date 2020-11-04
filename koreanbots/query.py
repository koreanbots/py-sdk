import collections
from .enums import Scheme
import secrets


class QuerySet:
    def __init__(self, *args) -> None:
        self._Queryset: dict = collections.defaultdict(list)

        for _Query in args:
            self._Queryset[_Query.scheme].append(_Query)

    def __add__(self, other) -> None:
        if isinstance(other, Query):
            self._Queryset[other.scheme].append(other)
        elif isinstance(other, type(self)):
            for scheme, _QuerySet in other._Queryset.items:
                self._Queryset[scheme].append(_QuerySet)
        else:
            raise TypeError

        return self

    def __sub__(self, other) -> None:
        if isinstance(other, Query):
            self._Queryset[other.scheme].remove(other)
        elif isinstance(other, type(self)):
            for scheme, _QuerySet in other._Queryset.items:
                self._Queryset[scheme].remove(_QuerySet)
        else:
            raise TypeError

        return self

    @property
    def full_query(self) -> str:
        def generate_query(_Querysets: tuple) -> str:
            scheme, _Queryset = _Querysets

            return (
                f"{scheme} {{ {', '.join(map(lambda item: item.query, _Queryset))} }}"
            )

        return " ".join(map(generate_query, self._Queryset.items()))


class Query:
    def __init__(
        self, scheme: Scheme, name: str, args: dict = {}, returns: dict = {}
    ) -> None:
        self.id: str = secrets.token_hex(15)

        self.scheme: str = scheme.value
        self.name: str = name
        self.args: dict = args
        self.returns: dict = returns

    def __add__(self, other) -> None:
        if isinstance(other, type(self)):
            return QuerySet(self, other)
        elif isinstance(other, QuerySet):
            return other + self
        else:
            raise TypeError

    def __sub__(self, other) -> None:
        if isinstance(other, type(self)):
            raise ValueError
        elif isinstance(other, QuerySet):
            return other - self
        else:
            raise TypeError

    @property
    def query_args(self) -> str:
        def check_quote(value) -> str:
            if isinstance(value, str):
                return f'"{value}"'
            else:
                return str(value)

        return ", ".join(
            map(lambda item: f"{item[0]}: {check_quote(item[1])}", self.args.items())
        )

    @property
    def query_returns(self) -> str:
        return ", ".join(
            map(
                lambda item: item[0]
                if not item[1]
                else f"{item[0]} {{ {', '.join(item[1])} }}",
                self.returns.items(),
            )
        )

    @property
    def query(self) -> str:
        return f"{self.id}: {self.name} ({self.query_args}) {{ {self.query_returns} }}"

    @property
    def full_query(self) -> str:
        return f"{self.scheme} {{ {self.query} }}"


print(
    (
        Query(
            Scheme.Query,
            "bot",
            {"id": "123"},
            returns={"name": None, "owners": ["id", "avatar"]},
        )
        + Query(
            Scheme.Query,
            "bot",
            {"id": "456"},
            returns={"name": None, "owners": ["id", "avatar"]},
        )
        + Query(
            Scheme.Mutation,
            "bot",
            {"id": "789"},
            returns={"name": None},
        )
    ).full_query
)