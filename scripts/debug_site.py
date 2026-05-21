#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""站点与文档一致性检查（Debug 会话 c68ecd）"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG_PATH = ROOT / "debug-c68ecd.log"
SITE_STYLES = ROOT / "site" / "styles" / "main.css"
RESUME_HTML = ROOT / "docs" / "resume" / "index.html"
RESUME_MD = ROOT / "content" / "resume.md"
MANIFEST = ROOT / "content" / "articles" / "manifest.json"
DOCS_ARTICLES = ROOT / "docs" / "articles"

ZH_LEAK = re.compile(r"<h1>English</h1>|<h1>Wu Yaorui</h1>", re.I)


def log(hypothesis_id: str, location: str, message: str, data: dict) -> None:
    # #region agent log
    entry = {
        "sessionId": "c68ecd",
        "runId": "debug-site",
        "hypothesisId": hypothesis_id,
        "location": location,
        "message": message,
        "data": data,
        "timestamp": int(datetime.now(timezone.utc).timestamp() * 1000),
    }
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    # #endregion


def check_resume_locale_leak() -> bool:
    """H1: 中文简历块末尾混入 English / Wu Yaorui"""
    html = RESUME_HTML.read_text(encoding="utf-8")
    m = re.search(
        r'<div class="resume-locale is-active" data-lang="zh">.*?<div class="resume-body">(.*?)</div>\s*</div>',
        html,
        re.DOTALL,
    )
    zh_body = m.group(1) if m else ""
    leaked = bool(ZH_LEAK.search(zh_body))
    log("H1", "debug_site.py:check_resume_locale_leak", "zh resume body scan", {"leaked": leaked})
    return not leaked


def check_markers_in_md() -> bool:
    """H1b: resume.md 标记顺序"""
    text = RESUME_MD.read_text(encoding="utf-8")
    zi = text.find("<!-- RESUME_LANG:zh -->")
    ei = text.find("<!-- RESUME_LANG:en -->")
    ok = zi != -1 and ei != -1 and zi < ei
    en_before_english = ei < text.find("# English") if "# English" in text else True
    log(
        "H1",
        "debug_site.py:check_markers_in_md",
        "marker positions",
        {"zh_idx": zi, "en_idx": ei, "en_before_english": en_before_english, "ok": ok and en_before_english},
    )
    return ok and en_before_english


def check_articles_sync_build() -> bool:
    """H2/H3: manifest 与 docs 文章页数量一致"""
    import json as js

    manifest_count = 0
    if MANIFEST.is_file():
        manifest_count = len(js.loads(MANIFEST.read_text(encoding="utf-8")).get("articles", []))
    built = len([p for p in DOCS_ARTICLES.glob("ep-*/index.html")])
    ok = manifest_count == built and manifest_count > 0
    log(
        "H2",
        "debug_site.py:check_articles_sync_build",
        "article count",
        {"manifest": manifest_count, "built_pages": built, "ok": ok},
    )
    return ok


def check_base_url() -> bool:
    """H5: 生成的 HTML 站内链接均含 base_url"""
    bad = []
    for html_path in (ROOT / "docs").rglob("*.html"):
        content = html_path.read_text(encoding="utf-8")
        for href in re.findall(r'href="([^"]+)"', content):
            if href.startswith("/") and not href.startswith("/PersonWebsite"):
                bad.append({"file": str(html_path.relative_to(ROOT)), "href": href})
    ok = len(bad) == 0
    log("H5", "debug_site.py:check_base_url", "bad hrefs", {"count": len(bad), "samples": bad[:5], "ok": ok})
    return ok


def check_article_layout_css() -> bool:
    """H6: 文章详情与简历同宽（无 42rem 窄栏限制）"""
    css = SITE_STYLES.read_text(encoding="utf-8")
    narrow = re.search(
        r"article:not\(\.resume-page\)\s*\{[^}]*max-width:\s*var\(--content-max\)",
        css,
    )
    ok = narrow is None
    log(
        "H6",
        "debug_site.py:check_article_layout_css",
        "article full-width like resume",
        {"ok": ok, "narrow_rule": bool(narrow)},
    )
    return ok


def check_doc_drift() -> bool:
    """H4: PRD/README 仍写 EP 系列（与 UI 个人文章不一致）"""
    drift = []
    for rel in ("PRD.md", "README.md"):
        p = ROOT / rel
        if p.is_file() and "EP 系列" in p.read_text(encoding="utf-8"):
            drift.append(rel)
    ok = len(drift) == 0
    log("H4", "debug_site.py:check_doc_drift", "EP 系列 in docs", {"files": drift, "ok": ok})
    return ok


def main() -> int:
    if LOG_PATH.is_file():
        LOG_PATH.unlink()
    checks = [
        ("H1 简历中文无 English 泄漏", check_resume_locale_leak()),
        ("H1 简历 marker 顺序", check_markers_in_md()),
        ("H2/H3 文章 manifest=构建页数", check_articles_sync_build()),
        ("H5 base_url 链接", check_base_url()),
        ("H4 文档 EP 系列 用语", check_doc_drift()),
        ("H6 文章详情铺满（同简历）", check_article_layout_css()),
    ]
    failed = [name for name, ok in checks if not ok]
    log("SUMMARY", "debug_site.py:main", "run complete", {"failed": failed, "passed": len(checks) - len(failed)})
    print(f"[INFO] 日志: {LOG_PATH}")
    for name, ok in checks:
        print(f"  {'OK' if ok else 'FAIL'} {name}")
    if failed:
        print(f"[FAIL] {len(failed)} 项未通过")
        return 1
    print("[OK] 全部检查通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
