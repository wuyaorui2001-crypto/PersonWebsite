#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""读取 config/sections.yaml，构建静态站到 docs/"""

from __future__ import annotations

import json
import math
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

import markdown
import yaml

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "config" / "sections.yaml"
SITE_DIR = ROOT / "site"
DOCS_DIR = ROOT / "docs"
ARTICLES_DIR = ROOT / "content" / "articles"
MANIFEST_PATH = ARTICLES_DIR / "manifest.json"
RESUME_PATH = ROOT / "content" / "resume.md"

ZH_MARKER = "<!-- RESUME_LANG:zh -->"
EN_MARKER = "<!-- RESUME_LANG:en -->"

MD = markdown.Markdown(
    extensions=["extra", "sane_lists", "smarty"],
    extension_configs={"smarty": {"smart_quotes": True}},
)


def fill(template: str, **kwargs: str) -> str:
    out = template
    for key, value in kwargs.items():
        out = out.replace("{{" + key + "}}", str(value))
    return out


def load_config() -> dict:
    with CONFIG_PATH.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def strip_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    meta = yaml.safe_load(parts[1]) or {}
    return meta, parts[2].lstrip("\n")


def md_to_html(text: str) -> str:
    MD.reset()
    html = MD.convert(text)
    return re.sub(r"<!--.*?-->", "", html, flags=re.DOTALL).strip()


def split_resume(text: str) -> tuple[str, str, dict]:
    meta, body = strip_frontmatter(text)
    if ZH_MARKER not in body or EN_MARKER not in body:
        raise ValueError(f"resume.md 缺少 {ZH_MARKER} 或 {EN_MARKER}")
    before_zh, rest = body.split(ZH_MARKER, 1)
    zh_part, en_part = rest.split(EN_MARKER, 1)
    zh_md = (before_zh.strip() + "\n\n" + zh_part.strip()).strip()
    en_md = en_part.strip()
    # 去掉板块大标题，正文里保留姓名 h1
    zh_md = re.sub(r"^#\s*中文\s*\n+", "", zh_md, flags=re.MULTILINE)
    en_md = re.sub(r"^#\s*English\s*\n+", "", en_md, flags=re.MULTILINE)
    return md_to_html(zh_md), md_to_html(en_md), meta


def render_page(
    layout: str,
    *,
    title: str,
    description: str,
    content: str,
    base_url: str,
    site_title: str,
    owner_name: str,
    lang: str = "zh-CN",
    body_class: str = "",
    nav_active: str = "",
    extra_head: str = "",
    extra_scripts: str = "",
    year: str | None = None,
) -> str:
    nav = {"home": "", "resume": "", "articles": ""}
    if nav_active in nav:
        nav[nav_active] = 'aria-current="page"'
    return fill(
        layout,
        title=title,
        description=description,
        content=content,
        base_url=base_url,
        site_title=site_title,
        owner_name=owner_name,
        lang=lang,
        body_class=body_class,
        extra_head=extra_head,
        extra_scripts=extra_scripts,
        year=year or str(datetime.now().year),
        nav_home=nav["home"],
        nav_resume=nav["resume"],
        nav_articles=nav["articles"],
    )


def write_html(path: Path, html: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")


def copy_assets() -> None:
    styles_src = SITE_DIR / "styles"
    styles_dest = DOCS_DIR / "assets" / "styles"
    if styles_dest.exists():
        shutil.rmtree(styles_dest)
    shutil.copytree(styles_src, styles_dest)

    scripts_src = SITE_DIR / "assets" / "scripts"
    scripts_dest = DOCS_DIR / "assets" / "scripts"
    scripts_dest.mkdir(parents=True, exist_ok=True)
    for js in scripts_src.glob("*.js"):
        shutil.copy2(js, scripts_dest / js.name)


def load_articles() -> list[dict]:
    if MANIFEST_PATH.is_file():
        data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        return data.get("articles", [])
    md_files = sorted(ARTICLES_DIR.glob("ep-*.md"))
    articles = []
    for p in md_files:
        articles.append({"slug": p.stem, "display_title": p.stem, "ep": 0, "title": p.stem})
    return articles


def build_home(cfg: dict, layout: str, home_tpl: str) -> None:
    site = cfg["site"]
    meta, _ = strip_frontmatter(RESUME_PATH.read_text(encoding="utf-8"))
    owner = meta.get("name", site.get("title", "个人站"))
    headline = meta.get("headline", "")
    content = fill(
        home_tpl,
        owner_name=owner,
        headline=headline,
        base_url=site["base_url"],
    )
    html = render_page(
        layout,
        title="首页",
        description=headline or owner,
        content=content,
        base_url=site["base_url"],
        site_title=site["title"],
        owner_name=owner,
        nav_active="home",
    )
    write_html(DOCS_DIR / "index.html", html)


def build_resume(cfg: dict, layout: str, resume_tpl: str) -> None:
    site = cfg["site"]
    raw = RESUME_PATH.read_text(encoding="utf-8")
    zh_html, en_html, meta = split_resume(raw)
    owner = meta.get("name", site["title"])
    updated = meta.get("updated", "")
    content = fill(
        resume_tpl,
        resume_zh=zh_html,
        resume_en=en_html,
        updated=updated,
    )
    script_tag = (
        f'<script src="{site["base_url"]}assets/scripts/resume-i18n.js" defer></script>'
    )
    html = render_page(
        layout,
        title="简历",
        description=f"{owner} — 简历",
        content=content,
        base_url=site["base_url"],
        site_title=site["title"],
        owner_name=owner,
        body_class="resume-page",
        nav_active="resume",
        extra_scripts=script_tag,
    )
    write_html(DOCS_DIR / "resume" / "index.html", html)


def article_list_items(articles: list[dict], base_url: str) -> str:
    rows = []
    for a in articles:
        slug = a["slug"]
        title = a.get("display_title", slug)
        ep = a.get("ep", 0)
        rows.append(
            f'<li><a href="{base_url}articles/{slug}/">'
            f'<span class="ep-num">EP {ep:03d}</span>'
            f'<span class="ep-title">{title}</span></a></li>'
        )
    return "\n".join(rows) if rows else "<li>暂无文章，请先运行 sync_articles.py</li>"


def pagination_html(
    base_url: str,
    page: int,
    total_pages: int,
    list_path: str = "articles",
) -> str:
    if total_pages <= 1:
        return ""
    parts = ['<nav class="pagination" aria-label="分页">']
    if page > 1:
        prev = f"{base_url}{list_path}/" if page == 2 else f"{base_url}{list_path}/page/{page - 1}/"
        parts.append(f'<a href="{prev}">上一页</a>')
    for n in range(1, total_pages + 1):
        if n == page:
            parts.append(f'<span class="current">{n}</span>')
        elif n == 1:
            parts.append(f'<a href="{base_url}{list_path}/">{n}</a>')
        else:
            parts.append(f'<a href="{base_url}{list_path}/page/{n}/">{n}</a>')
    if page < total_pages:
        parts.append(f'<a href="{base_url}{list_path}/page/{page + 1}/">下一页</a>')
    parts.append("</nav>")
    return "\n".join(parts)


def build_articles(cfg: dict, layout: str, list_tpl: str, detail_tpl: str) -> None:
    site = cfg["site"]
    base_url = site["base_url"]
    section = next(s for s in cfg["sections"] if s["id"] == "articles")
    per_page = section.get("pagination", 30)
    articles = load_articles()
    articles.sort(key=lambda a: a.get("ep", 0))

    meta, _ = strip_frontmatter(RESUME_PATH.read_text(encoding="utf-8"))
    owner = meta.get("name", site["title"])

    total_pages = max(1, math.ceil(len(articles) / per_page))

    for page in range(1, total_pages + 1):
        chunk = articles[(page - 1) * per_page : page * per_page]
        items = article_list_items(chunk, base_url)
        pag = pagination_html(base_url, page, total_pages)
        content = fill(list_tpl, article_items=items, pagination=pag)
        html = render_page(
            layout,
            title="文章",
            description="EP 系列文章",
            content=content,
            base_url=base_url,
            site_title=site["title"],
            owner_name=owner,
            nav_active="articles",
        )
        if page == 1:
            write_html(DOCS_DIR / "articles" / "index.html", html)
        else:
            write_html(DOCS_DIR / "articles" / "page" / str(page) / "index.html", html)

    for a in articles:
        slug = a["slug"]
        md_path = ARTICLES_DIR / f"{slug}.md"
        if not md_path.is_file():
            print(f"[WARN] 缺少文章文件: {md_path}")
            continue
        body = md_path.read_text(encoding="utf-8")
        article_html = md_to_html(body)
        display = a.get("display_title", slug)
        content = fill(
            detail_tpl,
            article_title=display,
            article_meta=f"EP {a.get('ep', 0):03d}",
            article_body=article_html,
        )
        html = render_page(
            layout,
            title=display,
            description=display,
            content=content,
            base_url=base_url,
            site_title=site["title"],
            owner_name=owner,
            nav_active="articles",
        )
        write_html(DOCS_DIR / "articles" / slug / "index.html", html)


def main() -> int:
    if not CONFIG_PATH.is_file():
        print(f"[ERROR] 缺少配置: {CONFIG_PATH}")
        return 1
    if not RESUME_PATH.is_file():
        print(f"[ERROR] 缺少简历: {RESUME_PATH}")
        return 1

    cfg = load_config()
    layout = (SITE_DIR / "templates" / "layout.html").read_text(encoding="utf-8")
    home_tpl = (SITE_DIR / "templates" / "home.html").read_text(encoding="utf-8")
    resume_tpl = (SITE_DIR / "templates" / "resume.html").read_text(encoding="utf-8")
    list_tpl = (SITE_DIR / "templates" / "article_list.html").read_text(encoding="utf-8")
    detail_tpl = (SITE_DIR / "templates" / "article_detail.html").read_text(encoding="utf-8")

    if DOCS_DIR.exists():
        shutil.rmtree(DOCS_DIR)
    DOCS_DIR.mkdir(parents=True)

    copy_assets()

    for section in cfg.get("sections", []):
        if not section.get("enabled", True):
            continue
        sid = section["id"]
        if sid == "home":
            build_home(cfg, layout, home_tpl)
        elif sid == "resume":
            build_resume(cfg, layout, resume_tpl)
        elif sid == "articles":
            build_articles(cfg, layout, list_tpl, detail_tpl)

    built_at = datetime.now(timezone.utc).isoformat()
    print(f"[OK] 构建完成 -> {DOCS_DIR}")
    print(f"     时间: {built_at}")
    print(f"     预览: python scripts/preview.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
