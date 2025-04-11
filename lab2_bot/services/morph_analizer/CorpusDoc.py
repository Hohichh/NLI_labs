from docx import Document

from morph_analizer import Dictionary
from morph_analizer import nlp

class CorpusDoc:
    def __init__(self, doc: Document):
        self.title: str
        self.author: str
        self.topic: str = "Gastronomy"
        self.text: str = self.__load_text(doc)
        self.__marking = Dictionary(self.text)
    
    def __load_text(self, doc: Document) -> str:
        document = doc

        full_text = []
        for paragraph in document.paragraphs:
            full_text.append(paragraph.text)

        text = "\n".join(full_text)
        return text


    def __get_lemma_stats(self, word:str) -> int:
        #search all matches with word's lemma. 
        nltk_word = nlp(word)[0]
        counter: int = 0

        for lexeme in self.__marking.dictionary.values():
            if lexeme.lemma == nltk_word.lemma_:
                counter += lexeme.count

        return counter

    def __get_word_form_stats(self, word: str) -> int:
        #search all matches with current word form
        nltk_word = nlp(word)[0]
        counter: int = 0

        for word_form in self.__marking.dictionary.keys():
            if nltk_word.text == word_form:
                counter = self.__marking.dictionary[word_form].count
                return counter

    def __get_concordance_list(self, word:str) -> list[str]:
        #TODO : придумать как извлечь конкордансный список
        return "..." + word + "..."

    def pretty_print_stats(self, word: str):
        lemma_count = self.__get_lemma_stats(word)
        word_form_count = self.__get_word_form_stats(word)
        pass