from syntax_analizer import SyntaxTree, Node, nlp
from semantic_analizer import SemanticInfo, Predicate, predicate_parser, Dictionary
from .semantic_analizer.predicate_tags import PREDICATE_DEP_TAGS, ARGUMENT_DEP_TAGS

import aiofiles
from docx import Document
from pathlib import Path
import uuid

class NLPManager:
    def __init__(self, user_id:str):
        self.text = None
        self._sentences = None
        self._trees = None
        self._predicates = None
        self._dictionary = None
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
    def dictionary(self) -> Dictionary:
        if self.text is None:
            return None
        if self._dictionary is None:
            sem_dict = Dictionary(self.text)
            self._dictionary = sem_dict
        return self._dictionary

    @property
    def predicates(self) -> dict[Predicate]:
        pred_dict = {}
        trees = self.trees
        if trees is None:
            return None
        if self._predicates is None:
           for tree in trees:
                predicates = predicate_parser(tree)
                pred_dict[tree.sentence] = predicates
        self._predicates = pred_dict
        return self._predicates

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
        
    def get_sent_preds_json(self, ind:int) -> str:
        json_str = ""
        sentence = self.sentences[ind]
        predicates:list[Predicate] = self.predicates[sentence]
        json_str += sentence + "\n".join([pred.to_json() for pred in predicates])
        return json_str
    
    def word_sem_info_json(self, word:str) -> str:
        curr_word = self.dictionary.dictionary[word]
        json_str = curr_word.to_json()
        return json_str
    
    def update_word_sem_info(self, word:str, json_str:str) -> None:
        sem_info = self.dictionary.dictionary[word]
        sem_info.to_json(json_str)
        self.dictionary.dictionary[word] = sem_info
    

    




