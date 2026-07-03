"""格式清除：刪 CSS/字型/style，留章節結構、TOC、粗斜體、圖片。

刪檔案的同時必須清掉 OPF manifest 條目與 HTML 內的引用，不留懸空引用。
"""
from pathlib import Path

from lxml import etree

_PARSER = etree.XMLParser(recover=True, resolve_entities=False, no_network=True)

STYLE_FILE_SUFFIXES = {".css", ".ttf", ".otf", ".woff", ".woff2"}
HTML_SUFFIXES = {".xhtml", ".html", ".htm"}


def _clean_html(path: Path):
    tree = etree.parse(str(path), _PARSER)
    root = tree.getroot()
    if root is None:
        return
    for elem in list(root.iter()):
        if not isinstance(elem.tag, str):
            continue
        local = etree.QName(elem).localname
        if local == "style" or (
            local == "link"
            and elem.get("rel", "").lower() == "stylesheet"
        ):
            parent = elem.getparent()
            if parent is not None:
                parent.remove(elem)
        elif "style" in elem.attrib:
            del elem.attrib["style"]
    tree.write(str(path), xml_declaration=True, encoding="utf-8")


def _clean_manifest(opf_path: Path, deleted_names: set[str]):
    """從 manifest 移除已刪檔案的 item（用 href 檔名比對）。"""
    tree = etree.parse(str(opf_path), _PARSER)
    root = tree.getroot()
    if root is None:
        return
    for elem in list(root.iter()):
        if not isinstance(elem.tag, str):
            continue
        if etree.QName(elem).localname == "item":
            href = elem.get("href", "")
            if Path(href).name in deleted_names:
                elem.getparent().remove(elem)
    tree.write(str(opf_path), xml_declaration=True, encoding="utf-8")


def strip_format(root_dir: Path, on_log=lambda msg: None) -> None:
    root_dir = Path(root_dir)
    deleted: set[str] = set()
    for p in sorted(root_dir.rglob("*")):
        if p.is_file() and p.suffix.lower() in STYLE_FILE_SUFFIXES:
            deleted.add(p.name)
            p.unlink()
            on_log(f"刪除 {p.relative_to(root_dir).as_posix()}")
    for p in sorted(root_dir.rglob("*")):
        if p.is_file() and p.suffix.lower() in HTML_SUFFIXES:
            _clean_html(p)
            on_log(f"清樣式 {p.relative_to(root_dir).as_posix()}")
    for opf in root_dir.rglob("*.opf"):
        _clean_manifest(opf, deleted)
        on_log(f"清 manifest {opf.relative_to(root_dir).as_posix()}")
