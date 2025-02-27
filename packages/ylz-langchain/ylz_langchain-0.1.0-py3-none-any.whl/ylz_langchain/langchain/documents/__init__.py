from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ylz_langchain.langchain import LangchainLib

from ylz_langchain.langchain.documents.dir_loader import DirLoader
from ylz_langchain.langchain.documents.docx import DocxLib
from ylz_langchain.langchain.documents.image import ImageLib
from ylz_langchain.langchain.documents.pdf import PdfLib
from ylz_langchain.langchain.documents.pptx import PptxLib
from ylz_langchain.langchain.documents.url import UrlLib


class DocumentLib():
   def __init__(self,langchainLib:LangchainLib):
      self.dir = DirLoader(langchainLib)
      self.url = UrlLib(langchainLib)
      self.docx = DocxLib(langchainLib)
      self.pptx = PptxLib(langchainLib)
      self.image = ImageLib(langchainLib)
      self.pdf = PdfLib(langchainLib)