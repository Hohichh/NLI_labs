from .Rules.Noun import Noun
from .Rules.Verb import Verb
from .Rules.Adjective import Adjective
from .Rules.Adverb import Adverb


class Lexeme:
    def __init__(self, lemma:str, pos:str):
        self.lemma = lemma
        self.pos = pos
        self.ruler = self.__define_grammar(pos)
        self.count = 1

    def __define_grammar(self, pos:str):
        ruler = None
        if pos == "NOUN" or pos == "PROPN": 
            ruler = Noun()
        elif pos == "VERB" : 
            ruler = Verb()
        elif pos == "ADJ" : 
            ruler = Adjective()
        elif pos == "ADV" : 
            ruler = Adverb()
        
        return ruler
        
    def pretty_print(self):
        return f"Лемма слова: {self.lemma}\n\n" + self.ruler.pretty_print()