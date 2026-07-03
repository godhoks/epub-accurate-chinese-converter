"""文字轉換：Translator 介面＋OpenCC 實作＋整個 EPUB 目錄樹的轉換。

轉換範圍（spec）：內文 xhtml/html、toc.ncx、nav.xhtml、OPF metadata。
只轉文字節點（.text/.tail），不碰標籤名與屬性——href/src 引用檔名絕不能被轉。
"""
from abc import ABC, abstractmethod
from pathlib import Path

from lxml import etree
from opencc import OpenCC

from glossary import apply_glossary


class Translator(ABC):
    """翻譯引擎介面。Phase 2 中英翻譯實作同一介面。"""

    @abstractmethod
    def convert(self, text: str) -> str: ...


class OpenCCTranslator(Translator):
    # 只做字形轉換，不做用語在地化：專有名詞安全、不分地區。
    # 繁體採 OpenCC 最通用的繁體字形；想要特定用語（如軟體）用自訂詞彙表。
    CONFIGS = {"s2t": "s2tw", "t2s": "tw2s"}

    def __init__(self, direction: str):
        self._cc = OpenCC(self.CONFIGS[direction])

    def convert(self, text: str) -> str:
        return self._cc.convert(text)


_PARSER = etree.XMLParser(recover=True, resolve_entities=False, no_network=True)

TEXT_FILE_SUFFIXES = {".xhtml", ".html", ".htm", ".ncx"}


def _convert_node_text(elem, translate):
    if elem.text and elem.text.strip():
        elem.text = translate(elem.text)
    if elem.tail and elem.tail.strip():
        elem.tail = translate(elem.tail)


def _convert_xml_file(path: Path, translate, only_under_tag: str | None = None):
    """轉換一個 XML/XHTML 檔的文字節點。only_under_tag：僅轉該標籤（local name）底下。"""
    tree = etree.parse(str(path), _PARSER)
    root = tree.getroot()
    if root is None:
        return  # 解析完全失敗就跳過，不動原檔內容
    if only_under_tag:
        scopes = [e for e in root.iter()
                  if isinstance(e.tag, str) and etree.QName(e).localname == only_under_tag]
    else:
        scopes = [root]
    for scope in scopes:
        for elem in scope.iter():
            if not isinstance(elem.tag, str):
                continue  # 跳過註解/PI
            _convert_node_text(elem, translate)
    tree.write(str(path), xml_declaration=True, encoding="utf-8")


def convert_tree(root_dir: Path, translator: Translator,
                 glossary_pairs: list[tuple[str, str]],
                 on_log=lambda msg: None) -> None:
    """轉換整個解包後的 EPUB：內文、TOC、OPF metadata。glossary 在 OpenCC 之後套用。"""

    def translate(text: str) -> str:
        return apply_glossary(translator.convert(text), glossary_pairs)

    root_dir = Path(root_dir)
    for p in sorted(root_dir.rglob("*")):
        if not p.is_file():
            continue
        if p.suffix.lower() in TEXT_FILE_SUFFIXES:
            _convert_xml_file(p, translate)
            on_log(f"轉換 {p.relative_to(root_dir).as_posix()}")
        elif p.suffix.lower() == ".opf":
            _convert_xml_file(p, translate, only_under_tag="metadata")
            on_log(f"轉換 metadata {p.relative_to(root_dir).as_posix()}")
