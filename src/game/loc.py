from enum import Enum, auto

class Language(Enum):
    EN = auto()
    NYA = auto()

class Loc:
    def __init__(self, en: str, nya: str) -> None:
        self.lookup: dict[Language, str] = {Language.EN: en, Language.NYA: nya}

    def str(self, lang: Language) -> str:
        return self.lookup.get(lang, "MISSING TRANSLATION")

