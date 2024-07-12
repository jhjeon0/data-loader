import os
from langchain_core.documents import Document

from fastapi import HTTPException

from extension_enum import ExtensionEnum
from base import DataLoaderFactory


# pylint: disable=too-few-public-methods
class DataLoader:
    @classmethod
    def _file_exists_check(cls, file_path):
        if os.path.exists(file_path):
            return True

        raise HTTPException(detail="check your path", status_code=400)

    @classmethod
    def _file_extension_check(cls, extension):
        if extension.lower() in ExtensionEnum.list():
            return True

        raise HTTPException(
            detail="check your file`s extension",
            status_code=400,
        )

    @classmethod
    def data_loader(cls, file_path) -> list[Document]:
        _, extension = os.path.splitext(file_path)

        cls._file_exists_check(file_path)
        cls._file_extension_check(extension)

        result = DataLoaderFactory().get_data_loader(file_path)
        return result
