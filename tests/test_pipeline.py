import hashlib
import zipfile
import pytest
import pipeline
from tests.fixture_epub import make_test_epub


def _sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_end_to_end_convert_original_untouched(tmp_path):
    """spec 測試5：原檔 hash 前後不變（安全底線）；預設轉換專有名詞安全。"""
    epub = make_test_epub(tmp_path / "book.epub")
    before = _sha256(epub)
    out = pipeline.convert_epub(epub, "s2t")
    assert _sha256(epub) == before
    assert out.name == "book_traditional.epub"
    with zipfile.ZipFile(out) as zf:
        assert zf.infolist()[0].filename == "mimetype"
        html = zf.read("OEBPS/chapter1.xhtml").decode("utf-8")
        assert "軟件" in html      # 只轉字形
        assert "馬哈希" in html     # 人名不被誤轉


def test_end_to_end_with_strip_and_glossary(tmp_path):
    epub = make_test_epub(tmp_path / "book.epub")
    gl = tmp_path / "terms.txt"
    gl.write_text("魯迅=周樹人\n", encoding="utf-8")
    out = pipeline.convert_epub(epub, "s2t", strip=True, glossary_path=gl)
    with zipfile.ZipFile(out) as zf:
        names = set(zf.namelist())
        assert "OEBPS/stylesheet.css" not in names
        assert "OEBPS/cover.png" in names
        html = zf.read("OEBPS/chapter1.xhtml").decode("utf-8")
        assert "周樹人" in html


def test_invalid_epub_no_output(tmp_path):
    """失敗時不留半成品輸出檔。"""
    bad = tmp_path / "bad.epub"
    bad.write_bytes(b"not a zip at all")
    with pytest.raises(Exception):
        pipeline.convert_epub(bad, "s2t")
    assert not (tmp_path / "bad_traditional.epub").exists()
