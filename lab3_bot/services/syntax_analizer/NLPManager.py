from .SyntaxTree import SyntaxTree
from .Node import Node
from NLPM import nlp

import aiofiles
from docx import Document
import asyncio
import os


class NLPManager:
    def __init__(self):
        self._text = None
        self._trees = None
        self.file_path = None

    async def load_docx(self, document: Document, save_path: str) -> None:
        self._text = "\n".join([para.text for para in document.paragraphs if para.text.strip()])

        async with aiofiles.open(save_path, "w", encoding="utf-8") as f:
            await f.write(self._text)

        self.file_path = save_path
        self._trees = None 

    @property
    def trees(self) -> list[SyntaxTree]:
        if self._trees is None:
            sentences = [sent.text.strip() for sent in nlp(self._text).sents if sent.text.strip()]
            self._trees = [SyntaxTree(sentence) for sentence in sentences]
        return self._trees

    def get_tree_json(self, sentence_idx: int) -> str:
        return self.trees[sentence_idx].tree_to_json()

    def get_forest_json(self) -> list[str]:
        return [tree.tree_to_json() for tree in self.trees]

    def update_tree_from_json(self, sentence_idx: int, tree_json_str: str) -> None:
        self.trees[sentence_idx] = SyntaxTree.json_to_tree(tree_json_str)
