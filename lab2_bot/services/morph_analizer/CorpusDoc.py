from docx import Document
import aiofiles

from .Dictionary import Dictionary, nlp
from .Lexeme import Lexeme
from lexicon import LEXICON_RU

class CorpusDoc:
    def __init__(self, path: str):
        self.title: str = ""
        self.author: str = ""
        self.topic: str = "Gastronomy"
        self._text: str = None
        self._marking: Dictionary = None
        self._path = path

    @property
    async def text(self) -> str:
        if self._text is None:
            async with aiofiles.open(self._path, encoding="utf-8") as file:
                self._text = await file.read()
        return self._text

    @property
    async def marking(self) -> Dictionary:
        if self._marking is None:
            self._marking = Dictionary(await self.text)
        return self._marking

    async def pretty_print_stats(self, word: str) -> str:
        lemma_count: str = str(await self.get_lemma_stats(word))
        word_form_count: str = str(await self.get_word_form_stats(word))
        concordance_list: str = "\n".join(await self.get_concordance_list(word))
        morph_info = await self.get_morph_info(word)

        return LEXICON_RU["doc_stats"].format(
            word_form=word,
            morph_str=morph_info,
            lemmas=lemma_count,
            forms=word_form_count,
            concordances=concordance_list
        )

    async def get_morph_info(self, word: str) -> str:
        marking = await self.marking  # Use the property here
        try:
            lexeme: Lexeme = marking.dictionary[word]
            return lexeme.pretty_print()
        except KeyError:
            nltk_word = nlp(word)[0]
            lexeme = Lexeme(nltk_word.lemma_, nltk_word.pos_)
            return lexeme.pretty_print()

    async def get_lemma_stats(self, word: str) -> int:
        nltk_word = nlp(word)[0]
        marking = await self.marking  # Use the property here
        counter: int = 0

        for lexeme in marking.dictionary.values():
            if lexeme.lemma == nltk_word.lemma_:
                counter += lexeme.count

        return counter

    async def get_word_form_stats(self, word: str) -> int:
        nltk_word = nlp(word)[0]
        marking = await self.marking  # Use the property here
        counter: int = 0

        for word_form in marking.dictionary.keys():
            if nltk_word.text == word_form:
                counter = marking.dictionary[word_form].count
                break

        return counter

    async def get_concordance_list(self, sub_str: str) -> list[str]:
        concordance_list = []
        text = await self.text  # Use the property here
        tokens = text.split()
        sub_tokens = sub_str.split()

        for i in range(len(tokens) - len(sub_tokens) + 1):
            tokens_cut_str = " ".join(tokens[i:i+len(sub_tokens)]).lower().replace(".", "")
            if sub_str.lower() in tokens_cut_str:
                concordance = self.__extract_context(tokens, i, i+len(sub_tokens)-1, 5)
                concordance_list.append(concordance)

        return concordance_list

    def __extract_context(self, tokens: list[str], st_ind: int, end_ind: int, context: int) -> str:
        left_context = tokens[:st_ind]
        if len(left_context) > context:
            left_context = left_context[st_ind - context:st_ind]

        if len(tokens[end_ind:]) < context:
            right_context = tokens[end_ind+1:]
        else:
            right_context = tokens[end_ind+1:end_ind+context+1]

        str_left_context = " ".join(left_context)
        str_right_context = " ".join(right_context)
        curr_substr = " ".join(tokens[st_ind:end_ind+1])

        return "..." + str_left_context + " " + curr_substr + " " + str_right_context + "..."
        

    