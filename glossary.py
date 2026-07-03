"""自訂詞彙表：一行一對「原詞=譯詞」。

注意：套用在 OpenCC 之後，所以「原詞」須寫 OpenCC 轉換後的字形
（例：想把預設結果「滑鼠」改成「鼠標」，寫 `滑鼠=鼠標`）。
"""
from pathlib import Path


def load_glossary(path: Path) -> list[tuple[str, str]]:
    """讀詞彙表。# 開頭與空行忽略；無 = 的行忽略；保留檔案順序。"""
    pairs = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        src, dst = line.split("=", 1)
        if src:
            pairs.append((src, dst))
    return pairs


def apply_glossary(text: str, pairs: list[tuple[str, str]]) -> str:
    for src, dst in pairs:
        text = text.replace(src, dst)
    return text
