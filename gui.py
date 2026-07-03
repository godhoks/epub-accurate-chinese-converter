"""tkinter GUI：選檔 → 選方向 → 勾選項 → 轉換，log 即時顯示，介面三語可切換。"""
import queue
import sys
import threading
import tkinter as tk
import tkinter.font as tkfont
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

import i18n
import pipeline

UI_FONT_FAMILY = "Microsoft JhengHei UI"  # 微軟正黑，中英皆清楚
UI_FONT_SIZE = 11


def _resource_path(rel: str) -> Path:
    """支援 PyInstaller 打包後的資源路徑（_MEIPASS）。"""
    base = getattr(sys, "_MEIPASS", None)
    return Path(base) / rel if base else Path(rel)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.lang = i18n.load_lang()
        self.geometry("640x580")
        self._setup_fonts()
        self._set_icon()
        # 持久狀態（切換語言重建介面時不清空）
        self.selected_files: list[str] = []  # 批次：實際選到的檔案清單
        self.var_file = tk.StringVar()  # 只負責顯示摘要（唯讀）
        self.var_direction = tk.StringVar(value="s2t")
        self.var_strip = tk.BooleanVar(value=False)
        self.var_glossary = tk.StringVar()
        self.var_lang = tk.StringVar(value=i18n.LANG_LABELS[self.lang])
        self._log_queue: queue.Queue[str] = queue.Queue()
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self._build_widgets()
        self.after(100, self._drain_log)

    def _setup_fonts(self):
        """把介面預設字換成微軟正黑並放大，中英都清楚（等寬字顯示中文會醜）。"""
        for name in ("TkDefaultFont", "TkTextFont", "TkMenuFont", "TkHeadingFont"):
            try:
                tkfont.nametofont(name).configure(family=UI_FONT_FAMILY, size=UI_FONT_SIZE)
            except tk.TclError:
                pass
        ttk.Style(self).configure(".", font=(UI_FONT_FAMILY, UI_FONT_SIZE))

    def _set_icon(self):
        try:
            self.iconbitmap(str(_resource_path("assets/icon.ico")))
        except Exception:
            pass  # 無圖標不影響功能

    def _tr(self, key, **kw):
        return i18n.t(self.lang, key, **kw)

    def _build_widgets(self):
        self.title(self._tr("title"))
        pad = {"padx": 10, "pady": 5}

        frm_top = ttk.Frame(self.container)
        frm_top.pack(fill="x", **pad)
        combo = ttk.Combobox(frm_top, width=10, state="readonly",
                             values=list(i18n.LANG_LABELS.values()),
                             textvariable=self.var_lang)
        combo.pack(side="right")
        combo.bind("<<ComboboxSelected>>", self._on_lang_change)
        # 地球符號：語言無關，讓任何語言的使用者都認得這是語言切換
        ttk.Label(frm_top, text="🌐", font=("Segoe UI Emoji", 12)).pack(side="right", padx=(0, 4))

        frm_file = ttk.Frame(self.container)
        frm_file.pack(fill="x", **pad)
        ttk.Label(frm_file, text=self._tr("epub_file")).pack(side="left")
        self.var_file.set(self._file_summary())
        ttk.Entry(frm_file, textvariable=self.var_file, state="readonly").pack(
            side="left", fill="x", expand=True)
        ttk.Button(frm_file, text=self._tr("browse"),
                   command=self._pick_file).pack(side="left")

        frm_dir = ttk.Frame(self.container)
        frm_dir.pack(fill="x", **pad)
        ttk.Label(frm_dir, text=self._tr("direction")).pack(side="left")
        ttk.Radiobutton(frm_dir, text=self._tr("s2t"),
                        variable=self.var_direction, value="s2t").pack(side="left")
        ttk.Radiobutton(frm_dir, text=self._tr("t2s"),
                        variable=self.var_direction, value="t2s").pack(side="left")

        frm_opt = ttk.Frame(self.container)
        frm_opt.pack(fill="x", **pad)
        ttk.Checkbutton(frm_opt, text=self._tr("strip"),
                        variable=self.var_strip).pack(anchor="w")

        frm_gl = ttk.Frame(self.container)
        frm_gl.pack(fill="x", **pad)
        ttk.Label(frm_gl, text=self._tr("glossary")).pack(side="left")
        ttk.Entry(frm_gl, textvariable=self.var_glossary).pack(
            side="left", fill="x", expand=True)
        ttk.Button(frm_gl, text=self._tr("browse"),
                   command=self._pick_glossary).pack(side="left")
        ttk.Label(self.container, foreground="gray",
                  text=self._tr("glossary_hint")).pack(anchor="w", padx=10)

        self.btn_run = ttk.Button(self.container, text=self._tr("run"),
                                  command=self._run)
        self.btn_run.pack(**pad)

        self.txt_log = tk.Text(self.container, height=12, state="disabled",
                               font=(UI_FONT_FAMILY, UI_FONT_SIZE))
        self.txt_log.pack(fill="both", expand=True, **pad)

    def _on_lang_change(self, _event=None):
        label_to_code = {v: k for k, v in i18n.LANG_LABELS.items()}
        self.lang = label_to_code.get(self.var_lang.get(), i18n.DEFAULT_LANG)
        i18n.save_lang(self.lang)
        for w in self.container.winfo_children():
            w.destroy()
        self._build_widgets()  # 重建介面，tk 變數保留原值

    def _file_summary(self) -> str:
        """依目前語言算出檔案欄顯示文字：無=空、單檔=路徑、多檔=已選 N 個。"""
        n = len(self.selected_files)
        if n == 0:
            return ""
        if n == 1:
            return self.selected_files[0]
        return self._tr("n_files", n=n)

    def _pick_file(self):
        paths = filedialog.askopenfilenames(filetypes=[("EPUB", "*.epub")])
        if paths:
            self.selected_files = list(paths)
            self.var_file.set(self._file_summary())

    def _pick_glossary(self):
        p = filedialog.askopenfilename(
            filetypes=[(self._tr("txt_filter"), "*.txt"),
                       (self._tr("all_filter"), "*.*")])
        if p:
            self.var_glossary.set(p)

    def _log(self, msg: str):
        self._log_queue.put(msg)

    def _drain_log(self):
        try:
            while True:
                msg = self._log_queue.get_nowait()
                self.txt_log.configure(state="normal")
                self.txt_log.insert("end", msg + "\n")
                self.txt_log.see("end")
                self.txt_log.configure(state="disabled")
        except queue.Empty:
            pass
        self.after(100, self._drain_log)

    def _run(self):
        if not self.selected_files:
            messagebox.showwarning(self._tr("warn_title"), self._tr("warn_no_file"))
            return
        self.btn_run.configure(state="disabled")
        threading.Thread(target=self._worker, daemon=True).start()

    def _worker(self):
        try:
            glossary = (Path(self.var_glossary.get())
                        if self.var_glossary.get().strip() else None)
            results = pipeline.convert_many(
                self.selected_files,
                self.var_direction.get(),
                strip=self.var_strip.get(),
                glossary_path=glossary,
                on_log=self._log,
            )
            ok = sum(1 for _, out, err in results if err is None)
            self._log(self._tr("batch_summary", ok=ok, fail=len(results) - ok))
        except Exception as e:
            self._log(self._tr("failed", err=e))
        finally:
            self.after(0, lambda: self.btn_run.configure(state="normal"))
