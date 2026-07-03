import pytest
from PIL import Image
import make_icon


def test_make_icon_produces_valid_multisize_ico(tmp_path):
    """圖標是開發時產物；無中文字型的環境（如 CI）跳過。"""
    try:
        out = make_icon.make_icon(tmp_path / "icon.ico")
    except FileNotFoundError:
        pytest.skip("環境無中文字型，跳過圖標產生測試")
    assert out.exists()
    with Image.open(out) as im:
        assert im.format == "ICO"
        assert (32, 32) in im.info.get("sizes", set())
