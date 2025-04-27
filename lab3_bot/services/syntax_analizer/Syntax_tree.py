from .Node import Node
from .NLPM import nlp
import json

class SyntaxTree:
    def __init__(self, sentence:str):
        self.root = self.__init_tree(sentence)

    def __init_tree(self, sentence:str) -> Node:
        tokens = nlp(sentence)
        marked_tokens = {}
        
        for token in tokens:
            node = Node(token.dep_,
                        text=token.text)
            marked_tokens[token] = node

        root = None
        for token in tokens:
            node: Node = marked_tokens[token]
            if token.head == token:
                root = node
            else:
                parent: Node = marked_tokens[token.head]
                node.set_parent(parent)
                parent.add_child(node)

 
        return root
    
    def tree_to_json(self):
        def node_to_json(node: Node) -> dict:
            return {
                "text": node.text,
                "tag": node.synt_tag,
                "children": [node_to_json(child) for child in node.get_children()]
            }

        json_dict = node_to_json(self.root)
        return json.dumps(json_dict)

    

        

    
    
        
