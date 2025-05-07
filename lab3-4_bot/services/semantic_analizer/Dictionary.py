from docx import Document
import spacy
from nltk.corpus import wordnet as wn

from ..syntax_analizer import nlp
from .SemanticInfo import SemanticInfo


POS_MAP = {
    "NOUN": wn.NOUN,
    "VERB": wn.VERB,
    "ADJ": wn.ADJ,
    "ADV": wn.ADV
}

class Dictionary:
    def __init__(self, text: str):
        self.dictionary = self.__form_dictionary(text)

    def __form_dictionary(self, text: str) -> dict[str, SemanticInfo]:
        tokenized_text = nlp(text)
        dictionary = {}

        for token in tokenized_text:
            if token.pos_ in {"PROPN", "NOUN", "VERB", "ADJ", "ADV"}:
                word = token.text
                if token.pos_ != "PROPN":
                    word = word.lower()

                sem_info = SemanticInfo(word)
                wn_pos = POS_MAP.get(token.pos_, None)

                # Получаем синсеты с учётом POS
                synsets = wn.synsets(word, pos=wn_pos) if wn_pos else wn.synsets(word)
                if synsets:
                    definitions = [syn.definition() for syn in synsets]
                    sem_info.add_definitions(*definitions)

                    synonyms = set()
                    for syn in synsets:
                        for lemma in syn.lemmas():
                            synonyms.add(lemma.name().replace("_", " "))
                    sem_info.add_synonyms(synonyms)

                    hypernyms = set()
                    for syn in synsets:
                        for hyper in syn.hypernyms():
                            for lemma in hyper.lemmas():
                                hypernyms.add(lemma.name().replace("_", " "))
                    sem_info.add_hypernyms(hypernyms)

                dictionary[word] = sem_info

        return dict(sorted(dictionary.items())) if dictionary else {}
    

    def pretty_print_keys(self) -> str:
        if not self.dictionary:
            raise ValueError("Empty dictionary")
            
        items = [
            f"{i}. {key}"
            for i, key in enumerate(self.dictionary.keys(), 1)
        ]
        return "\n".join(items)





    

