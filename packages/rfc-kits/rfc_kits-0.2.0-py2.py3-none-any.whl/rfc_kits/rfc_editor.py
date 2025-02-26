# coding:utf-8

import os
from typing import Optional
from urllib.parse import urljoin

from requests.exceptions import HTTPError
from xkits import Page


class RfcEditorPage(Page):
    BASE: str = "https://www.rfc-editor.org"

    def __init__(self, location: str, filepath: Optional[str] = None):
        super().__init__(urljoin(self.BASE, location))
        self.__filepath: str = filepath or location

    @property
    def filepath(self) -> str:
        return self.__filepath

    def save(self) -> bool:
        rewrite: bool = not os.path.isfile(self.filepath)
        dirname: str = os.path.dirname(self.filepath)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        try:
            datas: bytes = self.response.content
        except HTTPError:
            return False

        if not rewrite:
            with open(self.filepath, "rb") as rhdl:
                if rhdl.read() != datas:
                    rewrite = True

        if rewrite:
            with open(self.filepath, "wb") as whdl:
                whdl.write(datas)

        return os.path.isfile(self.filepath)


class RfcText(RfcEditorPage):
    def __init__(self, number: int):
        self.__file: str = f"rfc{number}.txt"
        super().__init__(os.path.join("rfc", self.file))

    @property
    def file(self) -> str:
        return self.__file


class RfcHtml(RfcEditorPage):
    def __init__(self, number: int):
        self.__file: str = f"rfc{number}.html"
        self.__link: str = os.path.join("rfc", f"rfc{number}")
        super().__init__(os.path.join("rfc", self.file))

    @property
    def file(self) -> str:
        return self.__file

    @property
    def link(self) -> str:
        return self.__link

    def save(self) -> bool:
        if not super().save():
            return False

        if not os.path.exists(self.link) or os.readlink(self.link) != self.file:  # noqa:E501
            os.symlink(self.file, self.link)

        return os.readlink(self.link) == self.file


class RfcPdf(RfcEditorPage):
    def __init__(self, number: int):
        self.__file: str = os.path.join("pdfrfc", f"rfc{number}.txt.pdf")
        super().__init__(self.file, os.path.join("rfc", self.file))

    @property
    def file(self) -> str:
        return self.__file


class RFC():
    def __init__(self, number: int):
        self.__number: int = number

    @property
    def number(self) -> int:
        return self.__number

    @property
    def text(self) -> RfcText:
        return RfcText(self.number)

    @property
    def html(self) -> RfcHtml:
        return RfcHtml(self.number)

    @property
    def pdfrfc(self) -> RfcPdf:
        return RfcPdf(self.number)


class BcpText(RfcEditorPage):
    def __init__(self, number: int):
        self.__file: str = os.path.join("bcp", f"bcp{number}.txt")
        super().__init__(self.file, os.path.join("rfc", self.file))

    @property
    def file(self) -> str:
        return self.__file


class BCP():
    def __init__(self, number: int):
        self.__number: int = number

    @property
    def number(self) -> int:
        return self.__number

    @property
    def text(self) -> BcpText:
        return BcpText(self.number)
