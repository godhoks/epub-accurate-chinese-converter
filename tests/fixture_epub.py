"""產生測試用最小合法 EPUB：3 章、含 CSS/字型/inline style、簡體內文與目錄。"""
import base64
import zipfile
from pathlib import Path

PNG_1X1 = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJ"
    "AAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
)

CONTAINER_XML = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>"""

CONTENT_OPF = """<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="uid">test-epub-001</dc:identifier>
    <dc:title>软件测试之书</dc:title>
    <dc:creator>鲁迅</dc:creator>
    <dc:language>zh-CN</dc:language>
  </metadata>
  <manifest>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
    <item id="ch1" href="chapter1.xhtml" media-type="application/xhtml+xml"/>
    <item id="ch2" href="chapter2.xhtml" media-type="application/xhtml+xml"/>
    <item id="ch3" href="chapter3.xhtml" media-type="application/xhtml+xml"/>
    <item id="css" href="stylesheet.css" media-type="text/css"/>
    <item id="font" href="font.ttf" media-type="font/ttf"/>
    <item id="img" href="cover.png" media-type="image/png"/>
  </manifest>
  <spine toc="ncx">
    <itemref idref="ch1"/>
    <itemref idref="ch2"/>
    <itemref idref="ch3"/>
  </spine>
</package>"""

TOC_NCX = """<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head><meta name="dtb:uid" content="test-epub-001"/></head>
  <docTitle><text>软件测试之书</text></docTitle>
  <navMap>
    <navPoint id="n1" playOrder="1">
      <navLabel><text>第一章 软件</text></navLabel><content src="chapter1.xhtml"/>
    </navPoint>
    <navPoint id="n2" playOrder="2">
      <navLabel><text>第二章 内存</text></navLabel><content src="chapter2.xhtml"/>
    </navPoint>
    <navPoint id="n3" playOrder="3">
      <navLabel><text>第三章 鼠标</text></navLabel><content src="chapter3.xhtml"/>
    </navPoint>
  </navMap>
</ncx>"""

NAV_XHTML = """<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head><title>目录</title></head>
<body>
<nav epub:type="toc"><h1>目录</h1>
<ol>
<li><a href="chapter1.xhtml">第一章 软件</a></li>
<li><a href="chapter2.xhtml">第二章 内存</a></li>
<li><a href="chapter3.xhtml">第三章 鼠标</a></li>
</ol></nav>
</body></html>"""

CHAPTER_TMPL = """<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>{title}</title>
<link rel="stylesheet" type="text/css" href="stylesheet.css"/>
<style>p {{ color: red; }}</style>
</head>
<body>
<h1>{title}</h1>
<p style="font-size:12px">这本书讲软件。鲁迅说，内存很重要。马哈希是人名。</p>
<p><b>粗体保留</b><img src="cover.png" alt="图"/></p>
</body></html>"""

STYLESHEET_CSS = "body { font-family: SimSun; }"
FAKE_FONT = b"\x00\x01\x00\x00fake-font-bytes"

CHAPTERS = {
    "chapter1.xhtml": "第一章 软件",
    "chapter2.xhtml": "第二章 内存",
    "chapter3.xhtml": "第三章 鼠标",
}


def make_test_epub(path: Path) -> Path:
    """在 path 建立最小合法 EPUB，回傳 path。mimetype 必須第一個且不壓縮。"""
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        zf.writestr("META-INF/container.xml", CONTAINER_XML, compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr("OEBPS/content.opf", CONTENT_OPF, compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr("OEBPS/toc.ncx", TOC_NCX, compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr("OEBPS/nav.xhtml", NAV_XHTML, compress_type=zipfile.ZIP_DEFLATED)
        for name, title in CHAPTERS.items():
            zf.writestr(f"OEBPS/{name}", CHAPTER_TMPL.format(title=title),
                        compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr("OEBPS/stylesheet.css", STYLESHEET_CSS, compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr("OEBPS/font.ttf", FAKE_FONT, compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr("OEBPS/cover.png", PNG_1X1, compress_type=zipfile.ZIP_DEFLATED)
    return path
