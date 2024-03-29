import sys
from typing import AnyStr, Callable, Iterator, Literal, TypeVar, overload

if sys.version_info >= (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias

from .._types import _AnyStr, _OutputMethodArg
from ..etree import _ElementTree
from ._element import _HANDLE_FAILURES, HtmlElement

_HtmlDoc_T = TypeVar("_HtmlDoc_T", str, bytes, HtmlElement)
_HtmlElemOrTree: TypeAlias = HtmlElement | _ElementTree[HtmlElement]

# These are HtmlMixin methods converted to standard functions,
# with element or HTML string as first argument followed by all
# pre-existing args. Quoting from source:
#
#   ... the function takes either an element or an HTML string.  It
#   returns whatever the function normally returns, or if the function
#   works in-place (and so returns None) it returns a serialized form
#   of the resulting document.
#
# Special Notes:
# 1. These funcs operate on attributes that only make sense on
#    normal HtmlElements; lxml raises exception otherwise.
# 2. Although extra 'copy' argument is available, it is intended
#    only for internal use by each function, not something to be
#    arbitrarily changed by users, thus not available in stub.
#
# HACK Interesting, a 15+ yrs bug remains undiscovered,
# probably nobody is using them at all?
# All these standalone link funcs make use of _MethodFunc
# internal class in html/__init__.py, which has bug when
# converting input data. If input is not Element, the class
# automatically converts input to Element via fromstring(),
# taking in all keyword args used in link function call.
# Many of these keywords are unknown to fromstring(),
# thus causing Exception. Workaround this using @overload.

@overload
def find_rel_links(
    doc: HtmlElement,
    rel: str,
) -> list[HtmlElement]: ...
@overload
def find_rel_links(
    doc: _AnyStr,
    rel: str,
    /,
) -> list[HtmlElement]: ...
@overload
def find_class(
    doc: HtmlElement,
    class_name: _AnyStr,
) -> list[HtmlElement]: ...
@overload
def find_class(
    doc: _AnyStr,
    class_name: _AnyStr,
    /,
) -> list[HtmlElement]: ...
@overload
def make_links_absolute(
    doc: HtmlElement,
    base_url: str | None = ...,
    resolve_base_href: bool = ...,
    handle_failures: _HANDLE_FAILURES | None = ...,
) -> HtmlElement: ...
@overload
def make_links_absolute(
    doc: AnyStr,
    base_url: str | None = ...,
    resolve_base_href: bool = ...,
    handle_failures: _HANDLE_FAILURES | None = ...,
    /,
) -> AnyStr: ...
@overload
def resolve_base_href(
    doc: HtmlElement,
    handle_failures: _HANDLE_FAILURES | None = ...,
) -> HtmlElement: ...
@overload
def resolve_base_href(
    doc: AnyStr,
    handle_failures: _HANDLE_FAILURES | None = ...,
    /,
) -> AnyStr: ...
def iterlinks(
    doc: _HtmlDoc_T,
) -> Iterator[tuple[HtmlElement, str | None, str, int]]: ...
@overload
def rewrite_links(
    doc: HtmlElement,
    link_repl_func: Callable[[str], str | None],
    resolve_base_href: bool = ...,
    base_href: str | None = ...,
) -> HtmlElement: ...
@overload
def rewrite_links(
    doc: AnyStr,
    link_repl_func: Callable[[str], str | None],
    resolve_base_href: bool = ...,
    base_href: str | None = ...,
    /,
) -> AnyStr: ...

#
# Tree conversion
#
def html_to_xhtml(html: _HtmlElemOrTree) -> None: ...
def xhtml_to_html(xhtml: _HtmlElemOrTree) -> None: ...

#
# Tree output
#
# 1. Encoding issue is similar to etree.tostring().
#
# 2. Unlike etree.tostring(), all arguments here are not explicitly
#    keyword-only. Using overload with no default value would be
#    impossible, as the two arguments before it has default value.
#    Need to make a choice here: enforce all arguments to be keyword-only.
#    Less liberal code, but easier to maintain in long term for users.
#
# 3. Although html.tostring() does not forbid method="c14n" (or c14n2),
#    calling tostring() this way would render almost all keyword arguments
#    useless, defeating the purpose of existence of html.tostring().
#    Besides, no c14n specific arguments are accepted here, so it is
#    better to let etree.tostring() handle C14N.
@overload  # encoding=str / "unicode"
def tostring(  # type: ignore[overload-overlap]
    doc: _HtmlElemOrTree,
    *,
    pretty_print: bool = ...,
    include_meta_content_type: bool = ...,
    encoding: type[str] | Literal["unicode"],
    method: _OutputMethodArg = ...,
    with_tail: bool = ...,
    doctype: str | None = ...,
) -> str: ...
@overload  # encoding="..." / None, no encoding arg
def tostring(
    doc: _HtmlElemOrTree,
    *,
    pretty_print: bool = ...,
    include_meta_content_type: bool = ...,
    encoding: str | None = ...,
    method: _OutputMethodArg = ...,
    with_tail: bool = ...,
    doctype: str | None = ...,
) -> bytes: ...

#
# Debug
#
def open_in_browser(
    doc: _HtmlElemOrTree, encoding: str | type[str] | None = ...
) -> None: ...
