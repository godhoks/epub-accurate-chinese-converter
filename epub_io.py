"""EPUB 解包與重打包。原檔只讀不寫；重打包遵守 mimetype 規範。"""
import zipfile
from pathlib import Path


class InvalidEpubError(Exception):
    """不是合法 EPUB（缺 mimetype 或 zip 損壞）。"""


SUFFIX = {"s2t": "_traditional", "t2s": "_simplified"}


def unpack(epub_path: Path, dest_dir: Path) -> Path:
    """解開 EPUB 到 dest_dir。非法 EPUB 拋 InvalidEpubError。"""
    try:
        with zipfile.ZipFile(epub_path) as zf:
            names = zf.namelist()
            if "mimetype" not in names:
                raise InvalidEpubError(f"{epub_path.name} 缺 mimetype，不是合法 EPUB")
            if zf.read("mimetype").strip() != b"application/epub+zip":
                raise InvalidEpubError(f"{epub_path.name} mimetype 內容不對")
            zf.extractall(dest_dir)
    except zipfile.BadZipFile as e:
        raise InvalidEpubError(f"{epub_path.name} 不是有效的 zip：{e}") from e
    return dest_dir


def repack(src_dir: Path, output_path: Path) -> Path:
    """把資料夾重打包成 EPUB：mimetype 第一個且 STORED，其餘 DEFLATED。"""
    src_dir = Path(src_dir)
    with zipfile.ZipFile(output_path, "w") as zf:
        zf.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        for p in sorted(src_dir.rglob("*")):
            if p.is_dir():
                continue
            rel = p.relative_to(src_dir).as_posix()
            if rel == "mimetype":
                continue
            zf.write(p, rel, compress_type=zipfile.ZIP_DEFLATED)
    return output_path


def output_path_for(input_path: Path, direction: str) -> Path:
    """book.epub + s2t → book_traditional.epub；已存在則加 (1)、(2)…"""
    input_path = Path(input_path)
    base = input_path.with_suffix("").name + SUFFIX[direction]
    candidate = input_path.parent / f"{base}.epub"
    n = 1
    while candidate.exists():
        candidate = input_path.parent / f"{base}({n}).epub"
        n += 1
    return candidate
