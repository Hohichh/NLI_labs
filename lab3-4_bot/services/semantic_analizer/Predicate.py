class Predicate:
    def __init__(self, head:str | None):
        self.head:str = head
        pass

    def to_json(self) -> str:
        pass

    def from_json(self, json_str:str) -> None:
        pass