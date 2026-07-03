"""產生程式圖標 assets/icon.ico（概念 A：藍綠底＋奶白「漢」字）。

開發時跑一次即可，產物 icon.ico 進 repo。需 Windows 中文字型。
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BG = (44, 110, 107)    # #2C6E6B 藍綠
FG = (244, 237, 224)   # #F4EDE0 奶白
GLYPH = "漢"
FONT_CANDIDATES = [
    r"C:\Windows\Fonts\msjh.ttc",    # 微軟正黑
    r"C:\Windows\Fonts\msyh.ttc",    # 微軟雅黑
    r"C:\Windows\Fonts\simhei.ttf",  # 黑體
]


def _load_font(size: int) -> ImageFont.FreeTypeFont:
    for path in FONT_CANDIDATES:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    raise FileNotFoundError("找不到中文字型，請確認 Windows 字型目錄")


def _draw(size: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=size // 5, fill=BG)
    font = _load_font(int(size * 0.62))
    bbox = d.textbbox((0, 0), GLYPH, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (size - w) / 2 - bbox[0]
    y = (size - h) / 2 - bbox[1]
    d.text((x, y), GLYPH, font=font, fill=FG)
    return img


def make_icon(out_path: Path) -> Path:
    sizes = [16, 32, 48, 256]
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    base = _draw(256)
    base.save(out_path, format="ICO", sizes=[(s, s) for s in sizes])
    return out_path


if __name__ == "__main__":
    p = make_icon(Path("assets/icon.ico"))
    print(f"已產生 {p}")
