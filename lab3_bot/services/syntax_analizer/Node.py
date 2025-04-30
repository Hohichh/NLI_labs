from __future__ import annotations

class Node:
    def __init__(self, tag: str = None, 
                 parent: Node = None, 
                 children: list[Node] = None, 
                 text: str = None,
                 num: int = None):
        self.synt_tag = tag
        self.text = text
        self.__parent = parent
        self.__children = children if children is not None else []
        self.num = num

    def set_parent(self, parent) -> None:
        self.__parent = parent

    def get_parent(self) -> Node:
        return self.__parent
    
    def set_children(self, children: list[Node]) -> None:
        self.__children = children

    def get_children(self) -> list[Node]:
        return self.__children
    
    def add_child(self, child: Node) -> None:
        self.__children.append(child)

    

    