from .Rules.Noun import Noun
from .Rules.Verb import Verb
from .Rules.Adjective import Adjective
from .Rules.Adverb import Adverb


class Lexeme:
    def __init__(self, lemma:str, pos:str):
        self.lemma = lemma
        self.pos = pos
        self.__define_grammar(pos)

    def __define_grammar(self, pos:str):
        self.ruler = None

        if pos == "NOUN" or pos == "PROPN": 
            self.ruler = Noun()
        elif pos == "VERB" : 
            self.ruler = Verb()
        elif pos == "ADJ" : 
            self.ruler = Adjective()
        elif pos == "ADV" : 
            self.ruler = Adverb()
        
        if self.ruler:
            self.endings = self.ruler.endings
        else:
            self.endings = {}
        
    def pretty_print(self):
        return f"Лемма слова: {self.lemma}\n\n" + self.ruler.pretty_print()