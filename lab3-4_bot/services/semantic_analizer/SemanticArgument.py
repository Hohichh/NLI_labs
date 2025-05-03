class SemanticArgument:
    def __init__(self, word:str | None):
        self.word = word
        self.synonyms = set()
        self.definitions = []
        self.hypernyms = set()

    def add_synonyms(self, *synonyms) -> None:
        for item in synonyms:
            if isinstance(item, (list, set, tuple)):
                self.synonyms.update(item)
            else:
                self.synonyms.add(item)

    def add_hypernyms(self, *hypernyms) -> None:
        for item in hypernyms:
            if isinstance(item, (list, set, tuple)):
                self.hypernyms.update(item)
            else:
                self.hypernyms.add(item)

    def add_definitions(self, *definitions) -> None:
        for item in definitions:
            if isinstance(item, (list, set, tuple)):
                self.definitions.extend(item)
            else:
                self.definitions.append(item)

    def to_json(self) -> str:
        pass

    def from_json(self, json_str:str) -> None:
        pass