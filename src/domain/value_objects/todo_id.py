from uuid import UUID, uuid4


class TodoId:
    def __init__(self, value: str):
        try:
            self.value = UUID(value)
        except ValueError:
            raise ValueError("Invalid TodoId format")

    @classmethod
    def generate(cls):
        return cls(str(uuid4()))

    def __str__(self) -> str:
        return str(self.value)

    def __eq__(self, other) -> bool:
        if not isinstance(other, TodoId):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)
