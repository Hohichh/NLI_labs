import json


class SemanticInfo:
    def __init__(self, word:str | None):
        self.word = word
        self._synonyms = set()
        self._definitions = []
        self._hypernyms = set()
    
    def to_dict(self) -> dict:
        return {"word":self.word, 
                "semantic_info": {"definitions": self._definitions,
                                  "synonyms" : list(self._synonyms), 
                                  "hypernyms" : list(self._hypernyms)
                                 }
                }

    def add_synonyms(self, *synonyms) -> None:
        for item in synonyms:
            if isinstance(item, (list, set, tuple)):
                self._synonyms.update(item)
            else:
                self._synonyms.add(item)

    def add_hypernyms(self, *hypernyms) -> None:
        for item in hypernyms:
            if isinstance(item, (list, set, tuple)):
                self._hypernyms.update(item)
            else:
                self._hypernyms.add(item)

    def add_definitions(self, *definitions) -> None:
        for item in definitions:
            if isinstance(item, (list, set, tuple)):
                self._definitions.extend(item)
            else:
                self._definitions.append(item)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(),indent=2, ensure_ascii=False)

    def from_json(self, json_str:str) -> None:
        json_dict = json.loads(json_str)
        self.word = json_dict["word"]
        sem_info_dict = json_dict["semantic_info"]
        self._synonyms = set(sem_info_dict["synonyms"])
        self._hypernyms = set(sem_info_dict["hypernyms"])
        self._definitions = sem_info_dict["definitions"]

