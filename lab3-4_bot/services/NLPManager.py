from syntax_analizer import SyntaxTree, Node, nlp
from semantic_analizer import Argument, Predicate
from .predicate_tags import PREDICATE_DEP_TAGS, ARGUMENT_DEP_TAGS

import aiofiles
from docx import Document
from pathlib import Path
import uuid

#TODO: трансляция предикатов в жсоны !!!!!!!!!!!!!!!!!

class NLPManager:
    def __init__(self, user_id:str):
        self.text = None
        self._sentences = None
        self._trees = None
        self._predicates = None
        self._user_id = user_id
        self.file_path = Path(__file__).resolve().parents[2] / "data" / self._user_id
        self.file_path.mkdir(parents=True, exist_ok=True)

    async def download_docx(self, document: Document) -> None:
        text = "\n".join([para.text for para in document.paragraphs if para.text.strip()])
        save_path = self.file_path / f"{uuid.uuid4()}.txt"
        async with aiofiles.open(save_path, "w", encoding="utf-8") as f:
            await f.write(text)
        self.curr_text_path = save_path
        self.text = text
        self._trees = None

    @property
    def predicates(self) -> list[Predicate]:
        pred_dict = {}
        trees = self.trees
        if trees is None:
            return None
        if self._predicates is None:
           for tree in trees:
                predicates = self.__create_predicates(tree)
                pred_dict[tree.sentence] = predicates
        self._predicates = pred_dict
        return self._predicates


    def __create_predicates(self, tree: SyntaxTree) -> list:
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
                    


    @property
    def sentences(self) -> list[str]:
        if self.text is None:
            return None
        if self._sentences is None:
            doc = nlp(self.text)
            sentences = [sent.text for sent in doc.sents]
            self._sentences = sentences
        return self._sentences

    @property
    def trees(self) -> list[SyntaxTree]:
        if self.sentences is None:
            return None
        if self._trees is None:
            sentences = [sent.text.strip() for sent in nlp(self.text).sents if sent.text.strip()]
            self._trees = [SyntaxTree(sentence) for sentence in sentences]
        return self._trees

    def get_tree_json(self, sentence_idx: int) -> str:
        return self.trees[sentence_idx].tree_to_json()

    def get_forest_json(self) -> list[str]:
        return [tree.tree_to_json() for tree in self.trees]

    async def update_tree_from_json(self, sentence_idx: int, tree_json_str: str) -> None:
        new_tree = SyntaxTree("")
        new_tree.json_to_tree(tree_json_str)
        self.trees[sentence_idx] = new_tree
        text = [tree.sentence for tree in self._trees]
        text = " ".join(text)
        async with aiofiles.open(self.curr_text_path, "w", encoding="utf-8") as f:
            await f.write(text)
        self.text = text


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
    def get_predicates_json(self) -> str:
        pass

    def update_predicates_json(self) -> str:
        pass

