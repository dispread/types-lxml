from gzip import GzipFile
from io import FileIO
from typing import overload

from .._types import SupportsGeturl, _FileReadSource
from . import LxmlError, _ElementOrTree, _Validator

class RelaxNGError(LxmlError): ...
class RelaxNGParseError(RelaxNGError): ...
class RelaxNGValidateError(RelaxNGError): ...

class RelaxNG(_Validator):
    @overload
    def __init__(self, etree: _ElementOrTree) -> None: ...
    @overload
    def __init__(
        self,
        etree: None = ...,
        *,
        file: _FileReadSource | SupportsGeturl | FileIO | GzipFile,
    ) -> None: ...
    def __call__(self, etree: _ElementOrTree) -> bool: ...
    @classmethod
    def from_rnc_string(cls, src: str, base_url: str | None = ...) -> RelaxNG: ...
