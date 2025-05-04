import json
from syntax_analizer import SyntaxTree, Node
from .predicate_tags import ARGUMENT_DEP_TAGS, PREDICATE_DEP_TAGS

class Predicate:
    def __init__(self, head:str | None):
        self.head:str = head
        self._args:dict = {}

    def to_dict(self) -> dict:
        return {"head":self.head,
                "args":self._args
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
            self._args[key] = val


def predicate_parser(tree: SyntaxTree) -> list:
        root = tree.root
        predicates = []
        def add_predicate(pred_list:list, node:Node):
            if node.synt_tag not in PREDICATE_DEP_TAGS:
                return
            
            predicate = Predicate(node.text)
            args = {}
            for child in node.get_children():
                tag = child.synt_tag
                value = child.text
                if tag in PREDICATE_DEP_TAGS:
                    add_predicate(pred_list, child)
                elif tag in ARGUMENT_DEP_TAGS:
                    args[tag] = value
                else:
                    continue
            predicate._args = args
            pred_list.append(predicate)

        add_predicate(predicates, root)
        return predicates