import zipfile
import pytest
import epub_io
from tests.fixture_epub import make_test_epub


def test_unpack_extracts_files(tmp_path):
    epub = make_test_epub(tmp_path / "book.epub")
    out = tmp_path / "unpacked"
    epub_io.unpack(epub, out)
    assert (out / "OEBPS" / "content.opf").exists()
    assert (out / "mimetype").read_text() == "application/epub+zip"


def test_unpack_rejects_invalid_epub(tmp_path):
    """缺 mimetype 的 zip 不是 EPUB，要明確報錯而不是繼續做出壞檔。"""
    bad = tmp_path / "bad.epub"
    with zipfile.ZipFile(bad, "w") as zf:
        zf.writestr("hello.txt", "not an epub")
    with pytest.raises(epub_io.InvalidEpubError):
        epub_io.unpack(bad, tmp_path / "out")


def test_repack_mimetype_first_and_stored(tmp_path):
    """重打包必須維持 EPUB 規範，否則部分閱讀器打不開（spec 測試3）。"""
    epub = make_test_epub(tmp_path / "book.epub")
    unpacked = tmp_path / "unpacked"
    epub_io.unpack(epub, unpacked)
    out = tmp_path / "repacked.epub"
    epub_io.repack(unpacked, out)
    with zipfile.ZipFile(out) as zf:
        infos = zf.infolist()
        assert infos[0].filename == "mimetype"
        assert infos[0].compress_type == zipfile.ZIP_STORED
        assert set(zf.namelist()) >= {"OEBPS/content.opf", "OEBPS/chapter1.xhtml"}


def test_output_path_suffix_and_no_overwrite(tmp_path):
    src = tmp_path / "book.epub"
    src.touch()
    assert epub_io.output_path_for(src, "s2t").name == "book_traditional.epub"
    assert epub_io.output_path_for(src, "t2s").name == "book_simplified.epub"
    (tmp_path / "book_traditional.epub").touch()
    assert epub_io.output_path_for(src, "s2t").name == "book_traditional(1).epub"
