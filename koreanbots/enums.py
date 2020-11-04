import enum


class Scheme(enum.Enum):
    Query: str = "query"
    Mutation: str = "mutation"