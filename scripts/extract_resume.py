#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 content/source/resume.pdf 抽取文本，输出到 content/source/resume_extracted.txt。
不会覆盖 content/resume.md（resume.md 为展示源，需人工或 Agent 结构化后写入）。

用法:
  python scripts/extract_resume.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = ROOT / "content" / "source" / "resume.pdf"
OUT_TXT = ROOT / "content" / "source" / "resume_extracted.txt"


def main() -> int:
    if not PDF_PATH.is_file():
        print(f"[ERROR] 未找到: {PDF_PATH}")
        return 1
    try:
        import fitz
    except ImportError:
        print("[ERROR] 请安装: pip install pymupdf")
        return 1

    doc = fitz.open(PDF_PATH)
    parts = [page.get_text() for page in doc]
    doc.close()
    text = "\n".join(parts).strip()
    OUT_TXT.write_text(text, encoding="utf-8")
    print(f"[OK] 已写入 {OUT_TXT} ({len(text)} 字符)")
    print("[INFO] 请对照抽取文本更新 content/resume.md，或让 Agent 按 PRD 第六节结构化")
    return 0


if __name__ == "__main__":
    sys.exit(main())
