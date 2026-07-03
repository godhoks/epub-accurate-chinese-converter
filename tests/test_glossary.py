import glossary


def test_load_glossary_parses_pairs_skips_comments(tmp_path):
    f = tmp_path / "terms.txt"
    f.write_text("# 註解行\n魯迅=周樹人\n\n滑鼠=鼠標\n", encoding="utf-8")
    assert glossary.load_glossary(f) == [("魯迅", "周樹人"), ("滑鼠", "鼠標")]


def test_load_glossary_ignores_malformed_lines(tmp_path):
    f = tmp_path / "terms.txt"
    f.write_text("沒有等號的行\n好詞=好譯\n", encoding="utf-8")
    assert glossary.load_glossary(f) == [("好詞", "好譯")]


def test_apply_glossary_replaces_all_occurrences():
    pairs = [("魯迅", "周樹人")]
    assert glossary.apply_glossary("魯迅說魯迅", pairs) == "周樹人說周樹人"
