import spacy 
import csv
from .Rules import noun_rules
import os
from pathlib import Path

#Грамматика существительных
class Noun:
    def __init__(self):
        #Окончания для стандартных форм
        self.endings = {
        "PLUR" : "s", #plural number - множественное число
        "SPOS" : "'s", #single posessive - одиночное притяжательное
        "PPOS" : "s'" #plural posessive -  множественное притяжательное
    }
        self.irregular_nouns = self.__load_nouns()
        self.rules = noun_rules
    """
        Возвращает форму по указанным параметрам - число и притяжательность
        типа с фронта нужно будет получить именно число, падеж и тп, которые выберет юзер,
        чтобы генерить слова, поэтому я сделала этот метод как обертку над
        self.__generate_forn(lemma, morph_tag)
    """
    def pretty_print(self) -> str:
        return ("Часть речи: Существительное (Noun)\n"
                "Окончания\n"
                "- s  --- Множественное число (plural number)\n"
                "- 's --- Единственное число, притяжательная форма (single posessive)\n"
                "- s' --- Множественное число, притяжательная форма (plural posessive)\n"
                )

    def generate_form(self, **morph_params) -> str:

        lemma = morph_params.get("lemma")
        number = morph_params.get("number")
        posessive = morph_params.get("posessive")

        if not all([lemma, number, posessive]):
            raise ValueError("All parameters must be provided.")

        #rules - многомерный словарь, где ключи - грамматические категории
        rule = self.rules[number][posessive]
        #получаем "сырую" строку с тегом, заменяем на сгенеренное по тегу слово
        form = rule.format(BASE=lemma, 
                           PLUR = self.__generate_form(lemma, "PLUR"),
                           SPOS = self.__generate_form(lemma, "SPOS"),
                           PPOS = self.__generate_form(lemma, "PPOS"))
        return form
    """
        Генерирует слово по морфологическому тегу morpth_tag,
        который выбирается на основе выбранных юзером категорий
    """
    def __generate_form(self, lemma:str, morph_tag:str) -> str:
        #здесь эксепшены слова типа mouse - mice
        if self.__isException(lemma):
            if morph_tag == 'PLUR':
                return self.__get_plural_form(lemma)
            if morph_tag == 'PPOS':
                plur = self.__get_plural_form(lemma)
                if plur[-1] == 's':
                    return plur + "'"
                else: 
                    return plur + self.endings['SPOS']
        return lemma + self.endings[morph_tag]
        
    def __load_nouns(self) -> list[list[str]]:
        current_dir = Path(__file__).parent
        file_path = current_dir / 'Exceptions' / 'irregular_nouns.csv'
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            data = [row for row in reader]
        return data
    
    def __isException(self, lemma:str) -> bool:
        for lexema in self.irregular_nouns:
            if(lemma.lower() == lexema[0].lower()): 
                return True
        return False

    def __get_plural_form(self, lemma:str):
        for lexema in self.irregular_nouns:
            if lemma.lower() == lexema[0].lower():
                return lexema[1]
        return lemma