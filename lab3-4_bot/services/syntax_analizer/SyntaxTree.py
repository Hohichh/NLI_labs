from .Node import Node
from .NLPM import nlp
import json

class SyntaxTree:
    def __init__(self, sentence:str):
        self.root = self.__init_tree(sentence)
        self._sentence = sentence

    @property
    def sentence(self) -> str:
        self._sentence = self.__restore_sentence()
        return self._sentence

    def __init_tree(self, sentence:str) -> Node:
        tokens = nlp(sentence)
        marked_tokens = {}
        
        for i, token in enumerate(tokens):
            node = Node(token.dep_,
                        text=token.text,
                        num=i)
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
    
    def tree_to_json(self) -> str:
        def node_to_json(node: Node) -> dict:
            return {
                "text": node.text,
                "tag": node.synt_tag,
                "num": node.num,
                "children": [node_to_json(child) for child in node.get_children()]
            }

        json_dict = node_to_json(self.root)
        return json.dumps(json_dict, indent=2, ensure_ascii=False)
    
    def json_to_tree(self, json_str:str) -> None:
        json_dict = json.loads(json_str)

        def json_to_node(data: dict) -> Node:
            node = Node(data["tag"],text=data["text"],num=data["num"])
            for child in data.get("children", []):
                child_node = json_to_node(child)
                child_node.set_parent(node)
                node.add_child(child_node)
            return node
        
        root = json_to_node(json_dict)
        self.root = root

    def __restore_sentence(self) -> str:
        nodes = []
        def collect_nodes(curr_node: Node, nodes_list: list) -> Node:
            nodes_list.append(curr_node)
            for child in curr_node.get_children():
                collect_nodes(child, nodes_list)

        collect_nodes(self.root,nodes)
        nodes.sort(key=lambda node: node.num)
        
        result = []
        for i, node in enumerate(nodes):
            if i == 0:
                result.append(node.text)
                continue
            
            prev_token = nodes[i - 1]

            if node.text in ",.:;!?)" or node.text.startswith("»"):
                result.append(node.text)
            elif prev_token.text in "«(":
                result.append(node.text)
            else:
                result.append(" " + node.text)
            
        return "".join(result)


        
        



        

    
    
        
