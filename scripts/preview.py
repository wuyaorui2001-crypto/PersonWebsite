#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""本地预览 docs/（需先 build；P4 后可用）"""

import http.server
import os
import socketserver
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
PORT = 8080


def main() -> int:
    if not (DOCS / "index.html").is_file():
        print("[WARN] docs/index.html 不存在，请先运行 python scripts/build.py")
        print(f"[INFO] 将尝试启动目录: {DOCS}")
    os.chdir(DOCS)
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"[OK] 预览: http://127.0.0.1:{PORT}/PersonWebsite/")
        print(f"     简历 http://127.0.0.1:{PORT}/PersonWebsite/resume/")
        print(f"     文章 http://127.0.0.1:{PORT}/PersonWebsite/articles/")
        print("Ctrl+C 停止")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
