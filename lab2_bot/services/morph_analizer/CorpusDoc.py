from docx import Document

from .Dictionary import Dictionary, nlp
from .Lexeme import Lexeme
from lexicon import LEXICON_RU

class CorpusDoc:
    def __init__(self, doc: Document):
        self.title: str = ""
        self.author: str = ""
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
        try:
            lexeme: Lexeme = self.__marking.dictionary[word]
            return lexeme.pretty_print()
        except KeyError:
            nltk_word = nlp(word)[0]
            lexeme = Lexeme(nltk_word.lemma_, nltk_word.pos_)
            return lexeme.pretty_print()

    
    def __load_text(self, doc: Document) -> str:
        document: Document = doc

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
                break
        
        return counter

    def get_concordance_list(self, sub_str:str) -> list[str]:
        concordance_list = []
        tokens = self.text.split() #слово / слово+запятая/точка / дефис
        sub_tokens = sub_str.split() #слово / слово+запятая/точка / дефис
        for i in range(len(tokens)-len(sub_tokens)+1):
            tokens_cut_str = " ".join(tokens[i:i+len(sub_tokens)]).lower().replace(".","")
            if sub_str.lower() in tokens_cut_str:
                concordance: str = self.__extract_context(tokens, i, i+len(sub_tokens)-1,5)
                concordance_list.append(concordance)

        return concordance_list
    

    def __extract_context(self, tokens: list[str], st_ind:int, end_ind, context: int) -> str:
        #for start/end of the text
        left_context = tokens[:st_ind]  
        if len(left_context) > context:  
            left_context = left_context[st_ind-context:st_ind]
        if len(tokens[end_ind:]) < context:
            right_context = tokens[end_ind+1:]
        else:
            right_context = tokens[end_ind+1:end_ind+context+1]
        
        #for start/end of the sentence
        str_left_context: str = " ".join(left_context)
        str_right_context: str = " ".join(right_context)
        curr_substr: str = " ".join(tokens[st_ind:end_ind+1])

        return "..." + str_left_context + " " + curr_substr + " " + str_right_context + "..."
        

    