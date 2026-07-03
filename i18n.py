"""介面語言（繁體中文/簡體中文/English）字串表與語言偏好記憶。

只影響介面文字，不影響 EPUB 轉換方向。偏好存在使用者家目錄一個純文字檔。
"""
from pathlib import Path

LANGS = ["zh_TW", "zh_CN", "en"]
DEFAULT_LANG = "zh_TW"
LANG_LABELS = {"zh_TW": "繁體中文", "zh_CN": "简体中文", "en": "English"}
_PREF_FILE = Path.home() / ".accuchineseconv_lang"

STRINGS = {
    "zh_TW": {
        "title": "EPUB Accurate Chinese Converter",
        "epub_file": "EPUB 檔（可多選）：",
        "n_files": "已選 {n} 個檔案",
        "batch_summary": "全部完成：{ok} 成功、{fail} 失敗",
        "browse": "選檔…",
        "direction": "方向：",
        "s2t": "簡 → 繁",
        "t2s": "繁 → 簡",
        "strip": "清除格式（刪樣式/字型，留章節、目錄、圖片）",
        "glossary": "詞彙表（選填）：",
        "glossary_hint": "詞彙表一行一對「原詞=譯詞」；原詞寫轉換後的字形（例：滑鼠=鼠標）",
        "run": "開始轉換",
        "warn_title": "提示",
        "warn_no_file": "請先選擇 EPUB 檔",
        "done": "✅ 輸出：{path}",
        "failed": "❌ 失敗：{err}",
        "txt_filter": "文字檔",
        "all_filter": "全部",
    },
    "zh_CN": {
        "title": "EPUB Accurate Chinese Converter",
        "epub_file": "EPUB 文件（可多选）：",
        "n_files": "已选 {n} 个文件",
        "batch_summary": "全部完成：{ok} 成功、{fail} 失败",
        "browse": "选择…",
        "direction": "方向：",
        "s2t": "简 → 繁",
        "t2s": "繁 → 简",
        "strip": "清除格式（删样式/字体，留章节、目录、图片）",
        "glossary": "词汇表（选填）：",
        "glossary_hint": "词汇表一行一对「原词=译词」；原词写转换后的字形（例：鼠标=滑鼠）",
        "run": "开始转换",
        "warn_title": "提示",
        "warn_no_file": "请先选择 EPUB 文件",
        "done": "✅ 输出：{path}",
        "failed": "❌ 失败：{err}",
        "txt_filter": "文本文件",
        "all_filter": "全部",
    },
    "en": {
        "title": "EPUB Accurate Chinese Converter",
        "epub_file": "EPUB files (multi-select):",
        "n_files": "{n} files selected",
        "batch_summary": "All done: {ok} succeeded, {fail} failed",
        "browse": "Browse…",
        "direction": "Direction:",
        "s2t": "Simplified → Traditional",
        "t2s": "Traditional → Simplified",
        "strip": "Strip formatting (remove styles/fonts, keep chapters, TOC, images)",
        "glossary": "Glossary (optional):",
        "glossary_hint": "One 'source=target' per line; source uses the post-conversion form",
        "run": "Convert",
        "warn_title": "Notice",
        "warn_no_file": "Please choose an EPUB file first",
        "done": "✅ Output: {path}",
        "failed": "❌ Failed: {err}",
        "txt_filter": "Text files",
        "all_filter": "All files",
    },
}


def load_lang() -> str:
    try:
        val = _PREF_FILE.read_text(encoding="utf-8").strip()
        if val in LANGS:
            return val
    except OSError:
        pass
    return DEFAULT_LANG


def save_lang(lang: str) -> None:
    if lang in LANGS:
        try:
            _PREF_FILE.write_text(lang, encoding="utf-8")
        except OSError:
            pass


def t(lang: str, key: str, **kwargs) -> str:
    text = STRINGS.get(lang, STRINGS[DEFAULT_LANG]).get(key, key)
    return text.format(**kwargs) if kwargs else text
