#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 thoughts/Article 同步 EP 系列到 content/articles/，生成 manifest.json"""

from __future__ import annotations

import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THOUGHTS_ARTICLE = Path(r"D:\Me&AI\Project\thoughts\Article")
OUT_DIR = ROOT / "content" / "articles"
MANIFEST_PATH = OUT_DIR / "manifest.json"
EP_PATTERN = re.compile(r"^EP\s*(\d+)\s+(.+)$", re.IGNORECASE)


def ep_slug(stem: str) -> str | None:
    m = EP_PATTERN.match(stem.strip())
    if not m:
        return None
    num = int(m.group(1))
    title = m.group(2).strip()
    title_slug = re.sub(r"\s+", "", title)
    return f"ep-{num:03d}-{title_slug}".lower()


def collect_sources() -> list[Path]:
    if not THOUGHTS_ARTICLE.is_dir():
        return []
    files = sorted(THOUGHTS_ARTICLE.glob("EP *.md"))
    return [p for p in files if EP_PATTERN.match(p.stem)]


def main() -> int:
    sources = collect_sources()
    if not sources:
        print(f"[ERROR] 未找到 EP 文章: {THOUGHTS_ARTICLE}/EP *.md")
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    entries: list[dict] = []

    for src in sources:
        slug = ep_slug(src.stem)
        if not slug:
            print(f"[WARN] 跳过无法解析的文件名: {src.name}")
            continue
        m = EP_PATTERN.match(src.stem)
        num = int(m.group(1))
        title = m.group(2).strip()
        dest = OUT_DIR / f"{slug}.md"
        shutil.copy2(src, dest)
        entries.append(
            {
                "slug": slug,
                "ep": num,
                "title": title,
                "display_title": f"EP {num:03d} | {title}",
                "source_file": src.name,
                "content_path": f"content/articles/{slug}.md",
            }
        )
        print(f"[OK] {src.name} -> {dest.name}")

    entries.sort(key=lambda x: x["ep"])
    manifest = {
        "synced_at": datetime.now(timezone.utc).isoformat(),
        "source_dir": str(THOUGHTS_ARTICLE),
        "articles": entries,
    }
    MANIFEST_PATH.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"[OK] manifest: {MANIFEST_PATH} ({len(entries)} 篇)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
