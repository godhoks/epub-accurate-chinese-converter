[![繁體中文](https://img.shields.io/badge/繁體中文-9E9E9E?style=for-the-badge)](README.md) [![English](https://img.shields.io/badge/English-2C6E6B?style=for-the-badge)](README.en.md)

# EPUB Accurate Chinese Converter

**Accurate · Reliable · Simple** — convert EPUB e-books between Simplified and Traditional Chinese in one click.

## Download

**[⬇ Download AccuChineseConv.exe (latest)](https://github.com/godhoks/epub-accurate-chinese-converter/releases/latest/download/AccuChineseConv.exe)**

Or see all versions on the [Releases page](https://github.com/godhoks/epub-accurate-chinese-converter/releases/latest). No installation — just download and run.

## Why this tool

- **Accurate**: character-level conversion, so proper nouns (like personal names) are never mistranslated; a custom glossary guarantees one consistent rendering of each term across the whole book.
- **Reliable**: never overwrites your original — always writes a new file; no half-finished output on failure; 25 automated tests and verified on real books.
- **Simple**: pick a file, pick a direction, click convert. No install, no setup. UI available in Traditional Chinese / Simplified Chinese / English.

## First run (Windows SmartScreen)

The first time you run it, Windows may show a blue "Windows protected your PC" dialog. This happens because independent open-source tools are not code-signed — it is **normal, not a virus**.

**What to do**: click "**More info**" → "**Run anyway**".

The tool runs entirely on your machine — no network access, no uploads — and never overwrites your original EPUB.

## Usage

1. Run `AccuChineseConv.exe`
2. Pick an EPUB file → choose a direction (Simplified → Traditional / Traditional → Simplified)
3. Optionally tick "Strip formatting" and pick a glossary
4. Click "Convert". The output is a new file `name_traditional.epub` / `name_simplified.epub`; your original is left untouched.

## Options

### Custom glossary (optional)

Forces a term to a rendering you choose, consistently across the whole book.
This tool only converts characters; if you prefer certain vocabulary, specify it in a glossary.

**Format**: a **UTF-8 plain-text `.txt`** file:

```
# Lines starting with # are comments
# One pair per line: source=target
軟件=軟體
記憶體=內存
```

**Important**: `source` must be written in its **post-conversion** form (the glossary is applied after character conversion). See `glossary_example.txt`.

### Strip formatting (optional)

Removes publisher CSS, embedded fonts and inline styles; keeps chapters, table of contents, bold/italic and images. Useful when the original layout is messy — the reader then applies its own clean style.

## Development

```bash
pip install -r requirements.txt
python -m pytest
python main.py
```
