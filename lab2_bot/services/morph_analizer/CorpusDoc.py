from docx import Document

from morph_analizer import Dictionary

class CorpusDoc:
    def __init__(self, doc: Document):
        self.title: str
        self.author: str
        self.topic: str = "Gastronomy"
        self.text: str = self.__load_text(doc)
        self.__dictionary = Dictionary(self.text)
    
    def __load_text(self, doc: Document) -> str:
        document = doc

        full_text = []
        for paragraph in document.paragraphs:
            full_text.append(paragraph.text)

        text = "\n".join(full_text)
        return text


    def __get_lemma_stats(self, word:str) -> int:
        #search all matches with word's lemma. 
        pass

    def __get_word_form_stats(self, word: str) -> int:
        #search all matches with current word form
        pass

    def __get_concordance_list(self, word:str) -> list[str]:
        pass

    def pretty_print_stats(self, word: str):
        #
        pass