from docx import Document

from morph_analizer import Dictionary, Lexeme
from morph_analizer import nlp
from lexicon import LEXICON_RU

class CorpusDoc:
    def __init__(self, doc: Document):
        self.title: str
        self.author: str
        self.topic: str = "Gastronomy"
        self.text: str = self.__load_text(doc)
        self.__marking = Dictionary(self.text)

    def pretty_print_stats(self, word: str) -> str:
        lemma_count:str = str(self.get_lemma_stats(word))
        word_form_count:str = str(self.get_word_form_stats(word))
        concordance_list:str = "\n".join(self.get_concordance_list(word))
        
        morph_info = self.get_morph_info(word)

        return LEXICON_RU["doc_stats"].format(word_form=word, 
                                              morph_str=morph_info,
                                              lemmas=lemma_count,
                                              forms=word_form_count,
                                              concordances=concordance_list)
    
    def get_morph_info(self, word:str) -> str:
        lexeme: Lexeme = self.__marking.dictionary[word]
        return lexeme.pretty_print()
    
    def __load_text(self, doc: Document) -> str:
        if not isinstance(doc, Document):
            raise ValueError

        document = doc

        full_text = []
        for paragraph in document.paragraphs:
            full_text.append(paragraph.text)

        text = "\n".join(full_text)
        return text

    def get_lemma_stats(self, word:str) -> int:
        #search all matches with word's lemma. 
        nltk_word = nlp(word)[0]
        counter: int = 0

        for lexeme in self.__marking.dictionary.values():
            if lexeme.lemma == nltk_word.lemma_:
                counter += lexeme.count

        return counter

    def get_word_form_stats(self, word: str) -> int:
        #search all matches with current word form
        nltk_word = nlp(word)[0]
        counter: int = 0

        for word_form in self.__marking.dictionary.keys():
            if nltk_word.text == word_form:
                counter = self.__marking.dictionary[word_form].count
                return counter

    def get_concordance_list(self, word:str) -> list[str]:
        concordance_list = []
        tokens = self.text.split() #слово / слово+запятая/точка / дефис
        for i, token in enumerate(tokens): 
            if token == word:
                concordance = self.__extract_context(tokens, i, 5)
                concordance_list.append(concordance)

        return concordance_list
    

    def __extract_context(self, tokens: list[str], i:int, context: int) -> str:
        #for start/end of the text
        if i - context < len(tokens[:i]):
            left_context = tokens[:-(i - context)+1]
        else:
            left_context = tokens[i-context:i]
        if len(tokens[i+1:]) < context:
            right_context = tokens[i+1:]
        else:
            right_context = tokens[i+1:i+context+1]
        
        #for start/end of the sentence
        str_left_context: str = " ".join(left_context)
        if "." in str_left_context:
            ind = str_left_context.rfind(".")
            str_left_context = str_left_context[ind:]
        
        str_right_context: str = " ".join(right_context)
        if "." in str_right_context:
            ind = str_right_context.index(".")
            str_right_context = str_right_context[:ind+1]

        return "..." + str_left_context + " " + tokens[i] + " " + str_right_context + "..."
        

    