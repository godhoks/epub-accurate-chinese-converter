import i18n


def test_all_languages_have_same_keys():
    """三語 key 必須一致，否則切語言會露出英文 key 或報 KeyError。"""
    base = set(i18n.STRINGS["zh_TW"])
    for lang in i18n.LANGS:
        assert set(i18n.STRINGS[lang]) == base, f"{lang} 的字串 key 與 zh_TW 不一致"


def test_load_lang_default_when_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(i18n, "_PREF_FILE", tmp_path / "nope")
    assert i18n.load_lang() == "zh_TW"


def test_save_then_load_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setattr(i18n, "_PREF_FILE", tmp_path / "lang")
    i18n.save_lang("en")
    assert i18n.load_lang() == "en"


def test_save_rejects_invalid_lang(tmp_path, monkeypatch):
    """非法語言碼不寫入，load 退回預設。"""
    monkeypatch.setattr(i18n, "_PREF_FILE", tmp_path / "lang")
    i18n.save_lang("fr")
    assert i18n.load_lang() == "zh_TW"


def test_t_formats_placeholder():
    assert i18n.t("en", "done", path="book.epub") == "✅ Output: book.epub"
