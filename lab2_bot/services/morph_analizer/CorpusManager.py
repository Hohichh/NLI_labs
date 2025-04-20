from docx import Document
from pathlib import Path
import uuid
import aiofiles

from .CorpusDoc import CorpusDoc
from lexicon import LEXICON_RU

class CorpusManager:
    def __init__(self, user_id: str): 
        self.user_id = user_id
        self.user_dir: str = Path(__file__).resolve().parents[2] / "corpus_data" / self.user_id
        self.user_dir.mkdir(parents=True, exist_ok=True)
        self.document_list: list[CorpusDoc] = []

    async def add_doc(self, doc: Document, title: str, author: str) -> bool:
        try:
            # взяли текст из ворд файла
            full_text = []
            for paragraph in doc.paragraphs:
                full_text.append(paragraph.text)

            text = "\n".join(full_text)

            path_to_text = self.user_dir / f"{uuid.uuid4()}.txt"
            async with aiofiles.open(path_to_text, "w", encoding="utf-8") as file:
                await file.write(text)  # записали

            corpusDoc = CorpusDoc(path_to_text)  # связываем инстанс класса с файлом
            corpusDoc.title = title
            corpusDoc.author = author

            self.document_list.append(corpusDoc)  # добавили в список доков
            return True
        except IOError as e:
            print(f"IO error: {e}")
        except Exception as e:
            print(f"something wrong: {e}")
        finally:
            return False

    def delete_doc(self, ind: int) -> bool:
        try:
            temp_doc = self.document_list.pop(ind)
            file_path = Path(temp_doc._path)
            file_path.unlink()  # синхронное удаление файла

            return True
        except FileNotFoundError:
            print(f"Файл {file_path} не найден.")
        except PermissionError:
            print(f"Нет прав для удаления файла {file_path}.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")
        finally:
            return False

    def get_doc(self, ind: int) -> CorpusDoc | None:
        try:
            corpus_doc = self.document_list[ind]
            return corpus_doc
        except IndexError:
            return None

    def get_docs_name_list(self) -> list[str]:
        name_list = []
        for doc in self.document_list:
            name_list.append(doc.title)

        return name_list

    async def pretty_print_stats(self, word: str) -> str:
        lemma_count: str = str(await self.__get_lemma_stats(word))  # добавлен await
        forms_count: str = str(await self.__get_word_form_stats(word))  # добавлен await
        concordance_list: str = "\n".join(await self.__get_concordance_list(word))  # добавлен await
        morph_info = await self.document_list[0].get_morph_info(word)  # добавлен await
        return LEXICON_RU["corpus_stats"].format(
            word_form=word,
            morph_str=morph_info,
            lemmas=lemma_count,
            forms=forms_count,
            concordances=concordance_list
        )

    async def __get_lemma_stats(self, word: str) -> int:
        lemmas = 0
        for doc in self.document_list:
            lemmas += await doc.get_lemma_stats(word)  # добавлен await

        return lemmas

    async def __get_word_form_stats(self, word: str) -> int:
        word_forms = 0
        for doc in self.document_list:
            word_forms += await doc.get_word_form_stats(word)  # добавлен await

        return word_forms

    async def __get_concordance_list(self, sub_str: str) -> list[str]:
        concordance_list = []
        for doc in self.document_list:
            concordance_list.extend(await doc.get_concordance_list(sub_str))  # добавлен await

        return concordance_list
