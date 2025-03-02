from __future__ import annotations

import re
import sys
from json import JSONDecodeError, loads
from typing import TYPE_CHECKING, Any, Final, Literal, cast

from anyio import Path as AsyncPath
from anyio import run_process

from kreuzberg import ValidationError
from kreuzberg._constants import MINIMAL_SUPPORTED_PANDOC_VERSION
from kreuzberg._mime_types import MARKDOWN_MIME_TYPE
from kreuzberg._string import normalize_spaces
from kreuzberg._sync import run_taskgroup
from kreuzberg._tmp import create_temp_file
from kreuzberg._types import ExtractionResult, Metadata
from kreuzberg.exceptions import MissingDependencyError, ParsingError

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Mapping
    from os import PathLike

if sys.version_info < (3, 11):  # pragma: no cover
    from exceptiongroup import ExceptionGroup  # type: ignore[import-not-found]

version_ref: Final[dict[str, bool]] = {"checked": False}

# Block-level node types in Pandoc AST
BLOCK_HEADER: Final = "Header"  # Header with level, attributes and inline content
BLOCK_PARA: Final = "Para"  # Paragraph containing inline content
BLOCK_CODE: Final = "CodeBlock"  # Code block with attributes and string content
BLOCK_QUOTE: Final = "BlockQuote"  # Block quote containing blocks
BLOCK_LIST: Final = "BulletList"  # Bullet list containing items (blocks)
BLOCK_ORDERED: Final = "OrderedList"  # Numbered list with attrs and items

# Inline-level node types in Pandoc AST
INLINE_STR: Final = "Str"  # Plain text string
INLINE_SPACE: Final = "Space"  # Single space
INLINE_EMPH: Final = "Emph"  # Emphasized text (contains inlines)
INLINE_STRONG: Final = "Strong"  # Strong/bold text (contains inlines)
INLINE_LINK: Final = "Link"  # Link with text and target
INLINE_IMAGE: Final = "Image"  # Image with alt text and source
INLINE_CODE: Final = "Code"  # Inline code span
INLINE_MATH: Final = "Math"  # Math expression

# Metadata node types in Pandoc AST
META_MAP: Final = "MetaMap"  # Key-value mapping of metadata
META_LIST: Final = "MetaList"  # List of metadata values
META_INLINES: Final = "MetaInlines"  # Inline content in metadata
META_STRING: Final = "MetaString"  # Plain string in metadata
META_BLOCKS: Final = "MetaBlocks"  # Block content in metadata

# Node content field name
CONTENT_FIELD: Final = "c"
TYPE_FIELD: Final = "t"

# Valid node types
NodeType = Literal[
    # Block types
    "Header",
    "Para",
    "CodeBlock",
    "BlockQuote",
    "BulletList",
    "OrderedList",
    # Inline types
    "Str",
    "Space",
    "Emph",
    "Strong",
    "Link",
    "Image",
    "Code",
    "Math",
    # Meta types
    "MetaMap",
    "MetaList",
    "MetaInlines",
    "MetaString",
    "MetaBlocks",
]

MIMETYPE_TO_PANDOC_TYPE_MAPPING: Final[Mapping[str, str]] = {
    "application/csl+json": "csljson",
    "application/docbook+xml": "docbook",
    "application/epub+zip": "epub",
    "application/rtf": "rtf",
    "application/vnd.oasis.opendocument.text": "odt",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
    "application/x-biblatex": "biblatex",
    "application/x-bibtex": "bibtex",
    "application/x-endnote+xml": "endnotexml",
    "application/x-fictionbook+xml": "fb2",
    "application/x-ipynb+json": "ipynb",
    "application/x-jats+xml": "jats",
    "application/x-latex": "latex",
    "application/x-opml+xml": "opml",
    "application/x-research-info-systems": "ris",
    "application/x-typst": "typst",
    "text/csv": "csv",
    "text/tab-separated-values": "tsv",
    "text/troff": "man",
    "text/x-commonmark": "commonmark",
    "text/x-dokuwiki": "dokuwiki",
    "text/x-gfm": "gfm",
    "text/x-markdown": "markdown",
    "text/x-markdown-extra": "markdown_phpextra",
    "text/x-mdoc": "mdoc",
    "text/x-multimarkdown": "markdown_mmd",
    "text/x-org": "org",
    "text/x-pod": "pod",
    "text/x-rst": "rst",
}

MIMETYPE_TO_FILE_EXTENSION_MAPPING: Final[Mapping[str, str]] = {
    "application/csl+json": "json",
    "application/docbook+xml": "xml",
    "application/epub+zip": "epub",
    "application/rtf": "rtf",
    "application/vnd.oasis.opendocument.text": "odt",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
    "application/x-biblatex": "bib",
    "application/x-bibtex": "bib",
    "application/x-endnote+xml": "xml",
    "application/x-fictionbook+xml": "fb2",
    "application/x-ipynb+json": "ipynb",
    "application/x-jats+xml": "xml",
    "application/x-latex": "tex",
    "application/x-opml+xml": "opml",
    "application/x-research-info-systems": "ris",
    "application/x-typst": "typst",
    "text/csv": "csv",
    "text/tab-separated-values": "tsv",
    "text/troff": "1",
    "text/x-commonmark": "md",
    "text/x-dokuwiki": "wiki",
    "text/x-gfm": "md",
    "text/x-markdown": "md",
    "text/x-markdown-extra": "md",
    "text/x-mdoc": "md",
    "text/x-multimarkdown": "md",
    "text/x-org": "org",
    "text/x-pod": "pod",
    "text/x-rst": "rst",
}


def _extract_inline_text(node: dict[str, Any]) -> str | None:
    if node_type := node.get(TYPE_FIELD):
        if node_type == INLINE_STR:
            return node.get(CONTENT_FIELD)
        if node_type == INLINE_SPACE:
            return " "
        if node_type in (INLINE_EMPH, INLINE_STRONG):
            return _extract_inlines(node.get(CONTENT_FIELD, []))
    return None  # pragma: no cover


def _extract_inlines(nodes: list[dict[str, Any]]) -> str | None:
    texts = [text for node in nodes if (text := _extract_inline_text(node))]
    result = "".join(texts).strip()
    return result if result else None


def _extract_meta_value(node: Any) -> str | list[str] | None:
    if not isinstance(node, dict) or CONTENT_FIELD not in node or TYPE_FIELD not in node:
        return None

    content = node[CONTENT_FIELD]
    node_type = node[TYPE_FIELD]

    if not content or node_type not in {
        META_STRING,
        META_INLINES,
        META_LIST,
        META_BLOCKS,
    }:
        return None

    if node_type == META_STRING and isinstance(content, str):
        return content

    if isinstance(content, list) and (content := [v for v in content if isinstance(v, dict)]):
        if node_type == META_INLINES:
            return _extract_inlines(cast(list[dict[str, Any]], content))

        if node_type == META_LIST:
            results = []
            for value in [value for item in content if (value := _extract_meta_value(item))]:
                if isinstance(value, list):  # pragma: no cover
                    results.extend(value)
                else:
                    results.append(value)
            return results

        # This branch is only taken for complex metadata blocks which we don't use
        if blocks := [block for block in content if block.get(TYPE_FIELD) == BLOCK_PARA]:  # pragma: no cover
            block_texts = []
            for block in blocks:
                block_content = block.get(CONTENT_FIELD, [])
                if isinstance(block_content, list) and (text := _extract_inlines(block_content)):
                    block_texts.append(text)
            return block_texts if block_texts else None

    return None


def _extract_metadata(raw_meta: dict[str, Any]) -> Metadata:
    meta: Metadata = {}

    for key, value in raw_meta.items():
        if extracted := _extract_meta_value(value):
            meta[key] = extracted  # type: ignore[literal-required]

    citations = [
        cite["citationId"]
        for block in raw_meta.get("blocks", [])
        if block.get(TYPE_FIELD) == "Cite"
        for cite in block.get(CONTENT_FIELD, [[{}]])[0]
        if isinstance(cite, dict)
    ]
    if citations:
        meta["citations"] = citations

    return meta


def _get_pandoc_type_from_mime_type(mime_type: str) -> str:
    if pandoc_type := (MIMETYPE_TO_PANDOC_TYPE_MAPPING.get(mime_type, "")):
        return pandoc_type

    if any(k.startswith(mime_type) for k in MIMETYPE_TO_PANDOC_TYPE_MAPPING):
        return next(
            MIMETYPE_TO_PANDOC_TYPE_MAPPING[k] for k in MIMETYPE_TO_PANDOC_TYPE_MAPPING if k.startswith(mime_type)
        )

    raise ValidationError(f"Unsupported mime type: {mime_type}")


async def _validate_pandoc_version() -> None:
    try:
        if version_ref["checked"]:
            return

        command = ["pandoc", "--version"]
        result = await run_process(command)

        version_match = re.search(r"pandoc\s+v?(\d+)\.\d+\.\d+", result.stdout.decode())
        if not version_match or int(version_match.group(1)) < MINIMAL_SUPPORTED_PANDOC_VERSION:
            raise MissingDependencyError("Pandoc version 2 or above is required")

        version_ref["checked"] = True

    except FileNotFoundError as e:
        raise MissingDependencyError("Pandoc is not installed") from e


async def _handle_extract_metadata(input_file: str | PathLike[str], *, mime_type: str) -> Metadata:
    pandoc_type = _get_pandoc_type_from_mime_type(mime_type)
    metadata_file, unlink = await create_temp_file(".json")
    try:
        command = [
            "pandoc",
            str(input_file),
            f"--from={pandoc_type}",
            "--to=json",
            "--standalone",
            "--quiet",
            "--output",
            str(metadata_file),
        ]

        result = await run_process(command)

        if result.returncode != 0:
            raise ParsingError("Failed to extract file data", context={"file": str(input_file), "error": result.stderr})

        json_data = loads(await AsyncPath(metadata_file).read_text("utf-8"))
        return _extract_metadata(json_data)
    except (RuntimeError, OSError, JSONDecodeError) as e:
        raise ParsingError("Failed to extract file data", context={"file": str(input_file)}) from e
    finally:
        await unlink()


async def _handle_extract_file(input_file: str | PathLike[str], *, mime_type: str) -> str:
    pandoc_type = _get_pandoc_type_from_mime_type(mime_type)
    output_path, unlink = await create_temp_file(".md")
    try:
        command = [
            "pandoc",
            str(input_file),
            f"--from={pandoc_type}",
            "--to=markdown",
            "--standalone",
            "--wrap=preserve",
            "--quiet",
        ]

        command.extend(["--output", str(output_path)])

        result = await run_process(command)

        if result.returncode != 0:
            raise ParsingError("Failed to extract file data", context={"file": str(input_file), "error": result.stderr})

        text = await AsyncPath(output_path).read_text("utf-8")

        return normalize_spaces(text)
    except (RuntimeError, OSError) as e:
        raise ParsingError("Failed to extract file data", context={"file": str(input_file)}) from e
    finally:
        await unlink()


async def process_file_with_pandoc(input_file: str | PathLike[str], *, mime_type: str) -> ExtractionResult:
    """Process a single file using Pandoc and convert to markdown.

    Args:
        input_file: The path to the file to process.
        mime_type: The mime type of the file.

    Raises:
        ParsingError: If the file data could not be extracted.

    Returns:
        ExtractionResult
    """
    await _validate_pandoc_version()

    _get_pandoc_type_from_mime_type(mime_type)

    try:
        metadata_task = _handle_extract_metadata(input_file, mime_type=mime_type)
        content_task = _handle_extract_file(input_file, mime_type=mime_type)
        results = await run_taskgroup(metadata_task, content_task)
        metadata, content = cast(tuple[Metadata, str], results)

        return ExtractionResult(
            content=normalize_spaces(content),
            metadata=metadata,
            mime_type=MARKDOWN_MIME_TYPE,
        )
    except ExceptionGroup as eg:
        raise ParsingError("Failed to process file", context={"file": str(input_file), "errors": eg.exceptions}) from eg


async def process_content_with_pandoc(content: bytes, *, mime_type: str) -> ExtractionResult:
    """Process content using Pandoc and convert to markdown.

    Args:
        content: The content to process.
        mime_type: The mime type of the content.

    Returns:
        ExtractionResult
    """
    extension = MIMETYPE_TO_FILE_EXTENSION_MAPPING.get(mime_type) or "md"
    input_file, unlink = await create_temp_file(f".{extension}")

    await AsyncPath(input_file).write_bytes(content)
    result = await process_file_with_pandoc(input_file, mime_type=mime_type)

    await unlink()
    return result
