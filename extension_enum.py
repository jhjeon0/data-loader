from enum import StrEnum


class ExtensionEnum(StrEnum):
    TXT = ".txt"
    DOCX = ".docx"
    DOC = ".doc"
    PDF = ".pdf"

    @classmethod
    def list(cls):
        return [c.value for c in cls]
