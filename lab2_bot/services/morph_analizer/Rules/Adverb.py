from .Adjective import Adjective
import csv
import re
import os
from pathlib import Path

class Adverb:
    def __init__(self):
        self.endings = {
        "CMP": ("more "),   # Comparative form
        "SCP": ("the most "),   # Superlative form
    }
        self.__adj_ruler = Adjective()

        self.__irregular_advs = self.__load_advs() 

    def pretty_print(self) -> str:
        return ("Часть речи: Наречие (Adverb)\n"
                "Приставки:\n"
                "- more  --- Сравнительная форма (Comparative)\n"
                "- the most --- Превосходная форма (Superlative)\n"
                )

    def generate_form(self, **morph_params) -> str:
        lemma = morph_params.get("lemma")
        degree = morph_params.get("degree")

        if not all([lemma, degree]):
            raise ValueError("All paramters must be provided.")

        morph_tag = ""
        if degree == "comparative":
            morph_tag = "CMP"
        elif degree == "superlative":
            morph_tag = "SCP"
        elif degree == 'positive':
            return lemma
        else:
            raise ValueError('Нужно указать 1 параметр: degree.')

        result = self.__generate_form(lemma, morph_tag)
        return result

    def __generate_form(self, lemma:str, morph_tag:str) -> str:
        if self.__is_exception(lemma):
            return self.__get_irregular(lemma, morph_tag)
        if self.__is_multisyllabic(lemma):
            return self.__get_multisyllabic_form(lemma, morph_tag)

        return self.__adj_ruler._Adjective__generate_form(lemma, morph_tag)


    def __is_multisyllabic(self, word: str) -> int:
        word = word.lower()
        vowels = "aeiouy"
        syllable_matches = re.findall(r'[aeiouy]+', word)

        if word.endswith('e'):
            syllable_count = len(syllable_matches) - 1
        else:
            syllable_count = len(syllable_matches)
        syllable_count = max(syllable_count, 1)
    
        return syllable_count > 1

        
    def __get_multisyllabic_form(self, lemma:str, morph_tag:str) -> str:
        return self.endings[morph_tag] + lemma.lower()
    
    def __is_exception(self, lemma:str) -> bool :
        for lexema in self.__irregular_advs:
            if lexema[0].lower() == lemma.lower():
                return True
        return False

    def __get_irregular(self, lemma:str, morph_tag:str) -> str:
        for lexema in self.__irregular_advs:
            if lexema[0].lower() == lemma.lower():
                if morph_tag == 'CMP':
                    return lexema[1].lower()
                if morph_tag == 'SCP':
                    return lexema[2].lower()
        return None
    
    def __load_advs(self) -> list[list[str]]:
        current_dir = Path(__file__).parent
        file_path = current_dir / 'Exceptions' / 'irregular_adverbs.csv'
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            data = [row for row in reader]
        return data
    
