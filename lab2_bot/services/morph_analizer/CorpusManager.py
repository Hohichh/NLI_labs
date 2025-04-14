from docx import Document

from .CorpusDoc import CorpusDoc
from lexicon import LEXICON_RU

class CorpusManager:
    def __init__(self): 
        self.document_list : list[CorpusDoc] = []

    def add_doc(self, doc: CorpusDoc) -> bool:
        try:
            self.document_list.append(doc)
            return True
        except Exception:
            return False

    def delete_doc(self, ind: int) -> bool:
        try:
            self.document_list.pop(ind)
            return True
        except IndexError:
            return False

    def get_doc(self, ind: int) -> CorpusDoc | None:
        try:
            corpus_doc = self.document_list[ind]
            return corpus_doc
        except IndexError:
            return None

    def get_docs_name_list(self) -> list[str]:
        name_list = []
        for doc in self.document_list:
            name_list.append(doc.title)
        
        return name_list

    def pretty_print_stats(self, word:str) -> str:
        lemma_count:str = str(self.__get_lemma_stats(word))
        forms_count:str = str(self.__get_word_form_stats(word))
        concordance_list:str = "\n".join(self.__get_concordance_list(word))
        morph_info = self.document_list[0].get_morph_info(word)
        return LEXICON_RU["corpus_stats"].format(word_form=word,
                                                 morph_str=morph_info,
                                                 lemmas=lemma_count,
                                                 forms=forms_count,
                                                 concordances=concordance_list)

    def __get_lemma_stats(self, word:str) -> int:
        lemmas = 0
        for doc in self.document_list:
            lemmas += doc.get_lemma_stats(word)

        return lemmas

    def __get_word_form_stats(self, word:str) -> int:
        word_forms = 0
        for doc in self.document_list:
            word_forms += doc.get_word_form_stats(word)

        return word_forms

    def __get_concordance_list(self, word:str) -> list[str]:
        concordance_list = []
        for doc in self.document_list:
            concordance_list.extend(doc.get_concordance_list(word))

        return concordance_list