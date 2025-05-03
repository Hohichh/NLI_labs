import json

from .Argument import Argument


class Predicate:
    def __init__(self, head:str | None):
        self.head:str = head
        self._args:dict = {}

    def to_dict(self) -> dict:
        return {"head":self.head,
                "args": {key: val.to_dict() if isinstance(val, Argument) else val
                 for key, val in self._args.items()}
                }

    def add_args(self, **kwargs) -> None:
        for key, value in kwargs.items():
            self._args[key] = value

    def get_val(self, arg:str) -> str:
        return self._args[arg]

    def to_json(self) -> str:
        return json.dumps(self.to_dict(),indent=2, ensure_ascii=False)

    def from_json(self, json_str:str) -> None:
        json_dict = json.loads(json_str)
        self.head = json_dict["head"]
        self._args = {}
        for key, val in json_dict["args"].items():
            arg = Argument(None)
            arg.from_json(json.dumps(val))
            self._args[key] = arg