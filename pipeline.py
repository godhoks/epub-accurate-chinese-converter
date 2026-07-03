"""流程編排：解包 → [格式清除] → 簡繁轉換＋詞彙表 → 重打包。

失敗時刪除不完整輸出；原檔永遠不動。
"""
import shutil
import tempfile
from pathlib import Path

import epub_io
import strip_format as strip_mod
from convert_text import OpenCCTranslator, convert_tree
from glossary import load_glossary


def convert_epub(input_path: Path, direction: str, strip: bool = False,
                 glossary_path: Path | None = None,
                 on_log=lambda msg: None) -> Path:
    """轉換一本 EPUB，回傳輸出檔路徑。direction: 's2t'（簡→繁）| 't2s'（繁→簡）。

    只做字形轉換，專有名詞安全；想要特定用語偏好用詞彙表。
    """
    input_path = Path(input_path)
    output_path = epub_io.output_path_for(input_path, direction)
    pairs = load_glossary(glossary_path) if glossary_path else []
    if pairs:
        on_log(f"詞彙表載入 {len(pairs)} 條")

    tmp = Path(tempfile.mkdtemp(prefix="accuchineseconv-"))
    try:
        on_log(f"解包 {input_path.name}")
        epub_io.unpack(input_path, tmp)
        if strip:
            on_log("格式清除…")
            strip_mod.strip_format(tmp, on_log)
        on_log("簡繁轉換…")
        convert_tree(tmp, OpenCCTranslator(direction), pairs, on_log)
        on_log("重打包…")
        epub_io.repack(tmp, output_path)
        on_log(f"完成：{output_path}")
        return output_path
    except Exception:
        output_path.unlink(missing_ok=True)  # 不留半成品
        raise
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def convert_many(input_paths, direction: str, strip: bool = False,
                 glossary_path: Path | None = None,
                 on_log=lambda msg: None):
    """批次轉換多本 EPUB。逐本進行，單本失敗不影響其他本。

    回傳 [(input_path, output_path 或 None, error 或 None), ...]。
    """
    results = []
    for raw in input_paths:
        p = Path(raw)
        try:
            out = convert_epub(p, direction, strip=strip,
                               glossary_path=glossary_path, on_log=on_log)
            results.append((p, out, None))
        except Exception as e:  # 單本失敗不中斷其他本
            on_log(f"❌ {p.name}：{e}")
            results.append((p, None, str(e)))
    return results
