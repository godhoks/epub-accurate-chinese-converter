import epub_io
import strip_format
from tests.fixture_epub import make_test_epub


def _stripped(tmp_path):
    epub = make_test_epub(tmp_path / "book.epub")
    root = epub_io.unpack(epub, tmp_path / "u")
    strip_format.strip_format(root)
    return root


def test_css_and_font_files_deleted_image_kept(tmp_path):
    root = _stripped(tmp_path)
    assert not (root / "OEBPS" / "stylesheet.css").exists()
    assert not (root / "OEBPS" / "font.ttf").exists()
    assert (root / "OEBPS" / "cover.png").exists()


def test_html_style_artifacts_removed_structure_kept(tmp_path):
    root = _stripped(tmp_path)
    html = (root / "OEBPS" / "chapter1.xhtml").read_text(encoding="utf-8")
    assert "<link" not in html
    assert "<style" not in html
    assert "style=" not in html
    assert "<h1>第一章 软件</h1>" in html      # 章節結構保留
    assert "<b>粗体保留</b>" in html            # 基本強調保留
    assert 'src="cover.png"' in html            # 圖片保留


def test_manifest_has_no_dangling_refs(tmp_path):
    """spec 測試2：刪掉的檔案不能還留在 manifest（懸空引用會讓閱讀器報錯）。"""
    root = _stripped(tmp_path)
    opf = (root / "OEBPS" / "content.opf").read_text(encoding="utf-8")
    assert "stylesheet.css" not in opf
    assert "font.ttf" not in opf
    assert "cover.png" in opf
    assert "chapter1.xhtml" in opf
