from docx import Document
import spacy

from .Lexeme import Lexeme
from .Rules.Adjective import Adjective
from .Rules.Adverb import Adverb
from .Rules.Verb import Verb
from .Rules.Noun import Noun

nlp = spacy.load("en_core_web_sm") #loading model

class Dictionary:
    def __init__(self, text: str):
        self.dictionary = self.__form_dictionary(text)

    def __form_dictionary(self, text: str) -> dict[Lexeme]:
        tokenized_text = nlp(text)
 
        dictionary = {}
        for token in tokenized_text:
            if token.pos_ in {"PROPN", "NOUN", "VERB", "ADJ", "ADV"}:
                lemma = token.lemma_
                pos = token.pos_
                text = token.text
                if token.pos_ != "PROPN":
                    lemma = lemma.lower()
                    text = text.lower()
                if text in dictionary:
                    dictionary[text].count += 1
                    # print(text + " --- " + str(dictionary[text].count))
                else:
                    dictionary[text] = Lexeme(lemma, pos)

        if not dictionary:
            return
        
        return dict(sorted(dictionary.items()))
    
    def generate_form(self, word, morph_params: dict):
        lexema = self.dictionary[word]
        morph_params["lemma"] = lexema.lemma
        return lexema.ruler.generate_form(**morph_params)

    def pretty_print_keys(self) -> str:
        if not self.dictionary:
            raise ValueError("Empty dictionary")
            
        items = [
            f"{i}. {key}"
            for i, key in enumerate(self.dictionary.keys(), 1)
        ]
        return "\n".join(items)

    def add_word(self, word_in:str):
        tokens = nlp(word_in)
        word = tokens[0]
        lexeme = Lexeme(word.lemma_, word.pos_)
        self.dictionary[word.text] = lexeme
        self.dictionary = dict(sorted(self.dictionary.items()))




    

