[![繁體中文](https://img.shields.io/badge/繁體中文-2C6E6B?style=for-the-badge)](README.md) [![简体中文](https://img.shields.io/badge/简体中文-9E9E9E?style=for-the-badge)](README.zh-CN.md) [![English](https://img.shields.io/badge/English-9E9E9E?style=for-the-badge)](README.en.md) [![License: MIT](https://img.shields.io/badge/License-MIT-4C9A2A?style=for-the-badge)](LICENSE)

# EPUB 精準漢字轉換器

**精準 · 可靠 · 簡單** — EPUB 簡體中文 ↔ 繁體中文互轉，並可一鍵清除雜亂排版。

## 下載

**[⬇ 前往下載最新版](https://github.com/godhoks/epub-accurate-chinese-converter/releases/latest)**

在 Releases 頁面點 `AccuChineseConv-vX.X.X.exe`（檔名含版號，方便辨識版本）即可。免安裝，下載即用。

## 為什麼選它

- **精準**：只轉字形，人名等專有名詞不會被誤轉；自訂詞彙表保證同一名詞全書同一譯法。
- **可靠**：永不覆寫原檔、一律輸出新檔；轉換失敗不留半成品；經自動化測試與真實書籍驗證。
- **簡單**：選檔 → 選方向 → 按轉換，三步完成。免安裝、免設定，介面支援繁體中文／簡體中文／English。
- **清爽**：可選一鍵清除出版社雜亂的 CSS／內嵌字型／樣式，只留章節、目錄、粗斜體、圖片，交給閱讀器乾淨顯示。

## 首次執行說明（Windows SmartScreen）

第一次執行時，Windows 可能跳出藍色的「Windows 已保護您的電腦」視窗。這是因為本工具是個人開源專案、沒有購買昂貴的數位簽章憑證，Windows 對**所有**未簽章程式都會這樣提示——與程式本身是否安全無關。

**你可以這樣確認它安全：**
- **原始碼全公開**：這個 repo 的每一行程式碼你都看得到，沒有隱藏行為
- **exe 由 GitHub 自動編譯**：不是誰手動上傳的檔案，是 GitHub Actions 直接從上面的公開原始碼打包產生（可在 Actions 紀錄查證），內容與原始碼一致
- **完全離線、不覆寫**：程式在你電腦本機執行，不連網、不上傳任何資料，也永遠不會動到你的原始 EPUB
- 仍不放心，可自行用防毒軟體或 [VirusTotal](https://www.virustotal.com/) 掃描這個 exe

確認後，點視窗裡的「**其他資訊**」→「**仍要執行**」即可。

## 使用

1. 執行 `AccuChineseConv.exe`
2. 選 EPUB 檔（可按 Ctrl／Shift 一次多選一批）→ 選方向（簡 → 繁 / 繁 → 簡）
3. 視需要勾「清除格式」、選詞彙表
4. 按「開始轉換」，完成後 log 顯示輸出路徑；輸出為新檔 `原名_traditional.epub` / `原名_simplified.epub`，原檔不會被動到

**批次轉換**：一次可選多本 EPUB，同一組方向／清除格式／詞彙表套用到整批；log 逐本顯示進度，最後總結「X 成功、Y 失敗」。某一本壞檔只會被跳過，不影響其他書。連書名（電子書 metadata）也會一起簡↔繁轉換。

## 選項說明

### 自訂詞彙表（選填）

強制某個詞全書統一成你要的譯法，程式保證整本書一致。
本工具只轉字形，若你偏好某些用語（例：把「軟件」都改成「軟體」），就用詞彙表指定。

**格式**：一個 **UTF-8 純文字檔（.txt）**，用記事本就能編輯：

```
# 井號開頭是註解，會被略過
# 一行一對：原詞=譯詞
軟件=軟體
記憶體=內存
```

**重要**：`原詞`要寫「**轉換之後**」的字形（詞彙表在字形轉換後才套用）。
用法：把檔案在 GUI「詞彙表」欄選進去即可。範例見 `glossary_example.txt`。

### 清除格式（選填）

刪除出版社的 CSS、內嵌字型、inline 樣式；保留章節、目錄、粗斜體、圖片。
適合原書排版雜亂時，讓閱讀器用自己的乾淨樣式顯示。

## 開發

```bash
pip install -r requirements.txt
python -m pytest
python main.py
```

## 授權

本專案採 [MIT License](LICENSE) 授權——可自由使用、修改、散布。
