import os
from abc import ABC
import fitz
from langchain_community.document_loaders.word_document import (
    UnstructuredWordDocumentLoader,
)
from langchain_core.documents import Document
from extension_enum import ExtensionEnum


class BaseDataLoader(ABC):
    registry: dict = {}

    @classmethod
    def register(cls, extension: ExtensionEnum):
        def add_loader(data_loader):
            if extension not in cls.registry:
                cls.registry[extension] = data_loader
            return data_loader

        return add_loader

    @classmethod
    def get_data_loader(cls, file_path: str):
        _, extension = os.path.splitext(file_path)
        docs = cls.registry[extension]().data_loader(file_path)
        return docs

    @classmethod
    def _get_document_from_fitz(cls, doc: fitz.Document, path: str) -> list[Document]:
        document_list = []
        for enum, page in enumerate(doc):
            document_list.append(
                Document(
                    page_content=page.get_text(),  # type: ignore
                    metadata={"source": path, "page": enum},
                )
            )
        if document_list[0].page_content == " \n":
            return []
        return document_list

    @classmethod
    def _get_document_from_docx(cls, doc: list[Document], path: str) -> list[Document]:
        document_list = []
        for enum, data in enumerate(doc):
            document_list.append(
                Document(
                    page_content=data.page_content,
                    metadata={"source": path, "page": enum},
                )
            )
        return document_list


class DataLoaderFactory(BaseDataLoader):
    @classmethod
    def get_data_loader(cls, file_path: str):
        docs = BaseDataLoader.get_data_loader(file_path)
        return docs


@BaseDataLoader.register(ExtensionEnum.TXT)
class TextDataLoader(BaseDataLoader):
    def data_loader(self, file_path):
        try:
            data = fitz.open(file_path)
            return self._get_document_from_fitz(data, file_path)
        except fitz.EmptyFileError:
            print(f"{file_path}: empty text file")
            return []


@BaseDataLoader.register(ExtensionEnum.PDF)
class PDFDataLoader(BaseDataLoader):
    def data_loader(self, file_path):
        data = fitz.open(file_path)
        return self._get_document_from_fitz(data, file_path)


@BaseDataLoader.register(ExtensionEnum.DOC)
class DocDataLoader(BaseDataLoader):
    def data_loader(self, file_path):
        loader = UnstructuredWordDocumentLoader(file_path, mode="paged")
        data = loader.load()
        return self._get_document_from_docx(data, file_path)


@BaseDataLoader.register(ExtensionEnum.DOCX)
class DocxDataLoader(BaseDataLoader):
    def data_loader(self, file_path):
        loader = UnstructuredWordDocumentLoader(file_path, mode="paged")
        data = loader.load()
        return self._get_document_from_docx(data, file_path)
