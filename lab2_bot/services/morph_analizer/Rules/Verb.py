import csv
from .Rules import verb_rules
import os
from pathlib import Path

#Грамматика глаголов
class Verb:

    def __init__(self):
        self.endings = {
        "3S": "s",   # 3rd person singular (present)
        "PAST": "ed",  # Past tensу
        "PART": "ed",  # Past participle
        "GER": "ing"  # Gerund/present participle
    }
        self.irregular_verbs = self.__load_verbs()
        self.doubling_letter_gerunds = self.__load_gerunds()
        self.doubling_letter_past = self.__load_doubling_past()
        self.rules = verb_rules
    '''
    абсолютно та же логика методов, что и c существительными
    изначально весь смысл этих словарей с правилами пошел именно от глаголов,
    тк я хотела попробовать не только менять сам глагол, но и подставлять
    всопомогательные глаголы am/is/are/did/has и тд...
    '''
    def pretty_print(self) -> str:
        return ("Часть речи: Глагол (Verb)\n"
                "Окончания\n"
                "- s  --- Множественное число, 3-е лицо, единственное число (3rd person singular (present))\n"
                "- ed --- Прошедшее время (Past tense)\n"
                "- ed --- Пассивный залог глагола(Past participle)\n"
                "- ing --- Герундий/настоящее продолженное время (Gerund/present participle)\n"
                )
    
    def generate_form(self, **morph_params) -> str:
        lemma = morph_params.get("lemma")
        tense = morph_params.get("tense")
        tense_type = morph_params.get("tense_type")
        number = morph_params.get("number")
        person = morph_params.get("person")
        voice = morph_params.get("voice")

        if not all([lemma, tense, tense_type, number, person, voice]):
            raise ValueError("All parameters must be provided.")
        #ужасающий пятимерный словарь 
        rule = self.rules[tense][tense_type][number][person][voice]
        form = rule.format(BASE=lemma,
                            PART=self.__generate_form(lemma, "PART"),
                            PAST=self.__generate_form(lemma, "PAST"), 
                            _3S=self.__generate_form(lemma, "3S"), 
                            GER=self.__generate_form(lemma, "GER"))
        
        return form

    def __generate_form(self, lemma: str, morph_tag: str) -> str:
        if self.__isException(lemma):
            if morph_tag == "PAST":
                return self.__get_past(lemma)
            if morph_tag == "PART":
                return self.__get_participle(lemma)
        if morph_tag == '3S':
            return self.__get_3rd_person_present(lemma) 
        if morph_tag == 'GER':
            return self.__get_gerund(lemma)
        
        if lemma[-1] == 'e':
            return lemma[:-1].lower() + self.endings[morph_tag] 

        return lemma.lower() + self.endings[morph_tag] 

    def __load_verbs(self) -> list[list[str]]:
        current_dir = Path(__file__).parent
        file_path = current_dir / 'Exceptions' / 'irregular_verbs.csv'
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            data = [row for row in reader]
        return data
    #слова у которых удваивается буква с ing
    def __load_gerunds(self) -> list[list[str]]:
        current_dir = Path(__file__).parent
        file_path = current_dir / 'Exceptions' / 'doubling_gerund.csv'
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            data = [row for row in reader]
        return data
    
    def __load_doubling_past(self) -> list[list[str]]:
        current_dir = Path(__file__).parent
        file_path = current_dir / 'Exceptions' / 'doubling_past.csv'
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            data = [row for row in reader]
        return data

    def __isException(self, lemma:str) -> bool:
        for lexema in self.irregular_verbs:
            if(lemma.lower() == lexema[0].lower()): 
                return True
            
        for lexema in self.doubling_letter_past:
            if lexema[0].lower() == lemma.lower():
                return True
        return False
    
    def __get_past(self, lemma: str) -> str:
    # Проверяем, является ли слово неправильным глаголом
        for lexema in self.irregular_verbs:
            if lexema[0].lower() == lemma.lower():
                return lexema[1].lower()
        
        # Проверяем, удваивается ли согласная
        for lexema in self.doubling_letter_past:
            if lexema[0].lower() == lemma.lower():
                return lexema[1].lower()
        
        # Если нет исключений, добавляем "ed"
        return lemma.lower() + self.endings["PAST"]

    def __get_participle(self, lemma:str) -> str:
        for lexema in self.irregular_verbs:
            if lexema[0].lower() == lemma.lower():
                return lexema[2].lower()
            
        for lexema in self.doubling_letter_past:
            if lexema[0].lower() == lemma.lower():
                return lexema[1].lower()
            
    def __get_3rd_person_present(self, lemma:str) -> str:
        if lemma[-1] in ['s','x','o'] or lemma[-2:] in ['ss', 'sh', 'ch']:
            return lemma.lower() + 'es'
        if lemma[-1] == 'y' and lemma[-2] not in ['a', 'o', 'e', 'u', 'i']:
            return lemma[:-1].lower() + 'ies' 
        return lemma.lower() + self.endings['3S']
    
    def __get_gerund(self, lemma:str) -> str:
        for lexema in self.doubling_letter_gerunds:
            if lemma.lower() == lexema[0].lower():
                return lexema[1].lower()
        if lemma[-1] == 'e':
            return lemma[:-1].lower() + 'ing'
        if lemma[-2:] == 'ie':
            return lemma[:-2].lower() + 'ying'
        return lemma.lower() + self.endings["GER"]