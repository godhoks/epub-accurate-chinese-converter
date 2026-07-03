import epub_io
import convert_text
from tests.fixture_epub import make_test_epub


def _unpacked(tmp_path):
    epub = make_test_epub(tmp_path / "book.epub")
    return epub_io.unpack(epub, tmp_path / "u")


def test_only_char_conversion_no_vocab_localization(tmp_path):
    """只轉字形、不做用語在地化 ⇒ 專有名詞安全。

    鎖住真書發現的 bug：用語在地化會把人名『马哈希』誤轉成『馬雜湊』。
    本工具刻意不做用語在地化，預設就不該發生這種事。
    """
    root = _unpacked(tmp_path)
    convert_text.convert_tree(root, convert_text.OpenCCTranslator("s2t"), [])
    html = (root / "OEBPS" / "chapter1.xhtml").read_text(encoding="utf-8")
    assert "軟件" in html            # 只轉字形（不做用語替換成「軟體」）
    assert "軟體" not in html
    assert "馬哈希" in html           # 人名不被誤轉
    assert "馬雜湊" not in html
    assert "软件" not in html
    assert 'src="cover.png"' in html  # 屬性（檔名引用）不能被轉


def test_toc_and_metadata_also_converted(tmp_path):
    """spec 測試1：防「內文繁、目錄/書名簡」。"""
    root = _unpacked(tmp_path)
    convert_text.convert_tree(root, convert_text.OpenCCTranslator("s2t"), [])
    assert "軟件" in (root / "OEBPS" / "toc.ncx").read_text(encoding="utf-8")
    assert "軟件" in (root / "OEBPS" / "nav.xhtml").read_text(encoding="utf-8")
    opf = (root / "OEBPS" / "content.opf").read_text(encoding="utf-8")
    assert "軟件測試之書" in opf     # dc:title
    assert "魯迅" in opf             # dc:creator
    assert 'href="chapter1.xhtml"' in opf  # manifest href 不能被轉


def test_glossary_applied_after_opencc(tmp_path):
    """spec 測試4：自訂詞彙表優先於 OpenCC 內建。"""
    root = _unpacked(tmp_path)
    convert_text.convert_tree(root, convert_text.OpenCCTranslator("s2t"),
                              [("魯迅", "周樹人")])
    html = (root / "OEBPS" / "chapter1.xhtml").read_text(encoding="utf-8")
    assert "周樹人" in html
    assert "魯迅" not in html


def test_t2s_char_conversion():
    """繁→簡只轉字形。"""
    assert convert_text.OpenCCTranslator("t2s").convert("軟體") == "软体"
