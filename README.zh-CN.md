[![繁體中文](https://img.shields.io/badge/繁體中文-9E9E9E?style=for-the-badge)](README.md) [![简体中文](https://img.shields.io/badge/简体中文-2C6E6B?style=for-the-badge)](README.zh-CN.md) [![English](https://img.shields.io/badge/English-9E9E9E?style=for-the-badge)](README.en.md) [![License: MIT](https://img.shields.io/badge/License-MIT-4C9A2A?style=for-the-badge)](LICENSE)

# EPUB 精准汉字转换器

**精准 · 可靠 · 简单** — EPUB 简体中文 ↔ 繁体中文互转，并可一键清除杂乱排版。

## 下载

**[⬇ 前往下载最新版](https://github.com/godhoks/epub-accurate-chinese-converter/releases/latest)**

在 Releases 页面点 `AccuChineseConv-vX.X.X.exe`（文件名含版号，方便辨识版本）即可。免安装，下载即用。

## 为什么选它

- **精准**：只转字形，人名等专有名词不会被误转；自定义词汇表保证同一名词全书同一译法。
- **可靠**：永不覆盖原文件、一律输出新文件；转换失败不留半成品；经自动化测试与真实书籍验证。
- **简单**：选文件 → 选方向 → 按转换，三步完成。免安装、免设置，界面支持繁体中文／简体中文／English。
- **清爽**：可选一键清除出版社杂乱的 CSS／内嵌字体／样式，只留章节、目录、粗斜体、图片，交给阅读器干净显示。

## 首次运行说明（Windows SmartScreen）

第一次运行时，Windows 可能弹出蓝色的「Windows 已保护你的电脑」窗口。这是因为本工具是个人开源项目、没有购买昂贵的数字签名证书，Windows 对**所有**未签名程序都会这样提示——与程序本身是否安全无关。

**你可以这样确认它安全：**
- **源代码全公开**：这个 repo 的每一行代码你都能看到，没有隐藏行为
- **exe 由 GitHub 自动编译**：不是谁手动上传的文件，是 GitHub Actions 直接从上面的公开源代码打包生成（可在 Actions 记录查证），内容与源代码一致
- **完全离线、不覆盖**：程序在你电脑本机运行，不联网、不上传任何数据，也永远不会动到你的原始 EPUB
- 仍不放心，可自行用杀毒软件或 [VirusTotal](https://www.virustotal.com/) 扫描这个 exe

确认后，点窗口里的「**更多信息**」→「**仍要运行**」即可。

## 使用

1. 运行 `AccuChineseConv.exe`
2. 选 EPUB 文件（可按 Ctrl／Shift 一次多选一批）→ 选方向（简 → 繁 / 繁 → 简）
3. 视需要勾「清除格式」、选词汇表
4. 按「开始转换」，完成后 log 显示输出路径；输出为新文件 `原名_traditional.epub` / `原名_simplified.epub`，原文件不会被动到

**批量转换**：一次可选多本 EPUB，同一组方向／清除格式／词汇表套用到整批；log 逐本显示进度，最后总结「X 成功、Y 失败」。某一本坏文件只会被跳过，不影响其他书。连书名（电子书 metadata）也会一起简↔繁转换。

## 选项说明

### 自定义词汇表（选填）

强制某个词全书统一成你要的译法，程序保证整本书一致。
本工具只转字形，若你偏好某些用语（例：把「軟件」都改成「軟體」），就用词汇表指定。

**格式**：一个 **UTF-8 纯文本文件（.txt）**，用记事本就能编辑：

```
# 井号开头是注释，会被略过
# 一行一对：原词=译词
軟件=軟體
記憶體=內存
```

**重要**：`原词`要写「**转换之后**」的字形（词汇表在字形转换后才套用）。
用法：把文件在 GUI「词汇表」栏选进去即可。示例见 `glossary_example.txt`。

### 清除格式（选填）

删除出版社的 CSS、内嵌字体、inline 样式；保留章节、目录、粗斜体、图片。
适合原书排版杂乱时，让阅读器用自己的干净样式显示。

## 开发

```bash
pip install -r requirements.txt
python -m pytest
python main.py
```

## 授权

本项目采用 [MIT License](LICENSE) 授权——可自由使用、修改、分发。
