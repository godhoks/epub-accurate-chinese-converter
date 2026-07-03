import zipfile
from tests.fixture_epub import make_test_epub


def test_fixture_mimetype_first_and_stored(tmp_path):
    """EPUB 規範：mimetype 是第一個條目且不壓縮——fixture 本身要合法，後面的測試才有意義。"""
    epub = make_test_epub(tmp_path / "test.epub")
    with zipfile.ZipFile(epub) as zf:
        infos = zf.infolist()
        assert infos[0].filename == "mimetype"
        assert infos[0].compress_type == zipfile.ZIP_STORED
        assert zf.read("mimetype") == b"application/epub+zip"


def test_fixture_contains_expected_files(tmp_path):
    epub = make_test_epub(tmp_path / "test.epub")
    with zipfile.ZipFile(epub) as zf:
        names = set(zf.namelist())
    assert "OEBPS/content.opf" in names
    assert "OEBPS/stylesheet.css" in names
    assert "OEBPS/font.ttf" in names
    assert "OEBPS/cover.png" in names
