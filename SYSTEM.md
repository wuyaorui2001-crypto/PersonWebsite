# SYSTEM - PersonWebsite AI 操作指南

> 版本: v0.2  
> 更新: 2026-05-21

---

## 30 秒速览

**PRD-first（强制）**：先读并更新 [`PRD.md`](PRD.md)，再改代码。Skill：`.cursor/skills/personwebsite-prd/SKILL.md`。

**站长日常发布**：见 PRD **§6.4**（本地改 content → push → Actions → Pages）；下文 SOP 为命令级步骤。

**这是什么**：个人品牌静态站 — 简历 + EP 文章，GitHub Pages 发布。

**内容源**：
- 简历：`content/resume.md`（主维护）；原件 `content/source/resume.pdf`
- 文章：从 `D:\Me&AI\Project\thoughts\Article\` 同步 `EP *.md` 到 `content/articles/`

**扩展方式**：改 `config/sections.yaml` 注册新板块，加 `content/<板块>/`，无需推翻构建器。

**改 UI**：必须先读 `frontend-design` skill，再改 `site/`。

---

## 标准 SOP

### 场景 A：用户更新简历 PDF

1. 若结构变化 → **先更新 PRD.md §4.1**
2. 确认 `content/source/resume.pdf`
3. `python scripts/extract_resume.py` → 查看 `resume_extracted.txt`
4. 更新 `content/resume.md`（保留 frontmatter/changelog）；正式工作追加在 `## 工作经历` **顶部**
5. `python scripts/build.py` → 按需 push

### 场景 B：用户只改简历文字（含入职后追加正式工作）

1. 只编辑 `content/resume.md`：`# 中文` 与 `# English` 两段同步改
2. 更新 `updated` 与 `changelog`
3. `python scripts/build.py`

### 场景 B2：简历中英切换（网页）

- 简历页固定按钮切换中文 / English（见 PRD 6.1.2）
- 构建时按 `<!-- RESUME_LANG:zh -->` / `<!-- RESUME_LANG:en -->` 从同一文件切出两段，由前端 JS 切换显示

### 场景 C：同步 EP 文章

1. `python scripts/sync_articles.py`
2. 检查 `content/articles/manifest.json`
3. `python scripts/build.py`

### 场景 D：新增板块（如工作复盘）

1. 在 `config/sections.yaml` 增加 section，`enabled: true`
2. 创建 `content/work-retrospective/` 并放入 Markdown
3. 如需新模板，在 `site/templates/` 增加并在 `build.py` 注册 builder
4. `python scripts/build.py`

### 场景 E：2000 篇规模压测

```bash
python scripts/benchmark_build.py
```

---

## 强制规则

| 检查项 | 规则 |
|--------|------|
| 文章内容 | 展示 thoughts 副本原文，构建时不调用 AI 改写 |
| 简历 | `resume.md` 为展示源；PDF 仅作抽取输入 |
| UI 修改 | 遵循 frontend-design skill，禁止 Inter/紫渐变等通用 AI 审美 |
| 文章排版 | 详情页 `.article-body` 对齐 thoughts `基础格式`（15px、行高 1.75 等） |
| 路径 | GitHub Pages 使用 `docs/` 下父子目录 `*/index.html` |
| Git | 仅在用户明确要求时 commit/push |

---

## 板块注册表

见 [`config/sections.yaml`](config/sections.yaml)。

当前启用：`home`、`resume`、`articles`  
预留：`work-retrospective`（`enabled: false`）

---

## 关联项目

| 项目 | 路径 |
|------|------|
| thoughts | `D:\Me&AI\Project\thoughts\` |
| agent-workspace | `D:\Me&AI\agent-workspace\` |

---

## GitHub Pages URL 结构

| 路径 | 文件 |
|------|------|
| `/PersonWebsite/` | `docs/index.html` |
| `/PersonWebsite/resume/` | `docs/resume/index.html` |
| `/PersonWebsite/articles/` | `docs/articles/index.html` |
| `/PersonWebsite/articles/page/1/` | `docs/articles/page/1/index.html` |
| `/PersonWebsite/articles/{slug}/` | `docs/articles/{slug}/index.html` |

---

## 脚本状态（P1）

| 脚本 | P1 | 说明 |
|------|-----|------|
| `extract_resume.py` | 占位 | P1b：PDF → resume.md |
| `sync_articles.py` | 占位 | P3：同步 EP |
| `build.py` | 占位 | P4：生成 docs/ |
| `benchmark_build.py` | 占位 | P3：2000 篇压测 |
| `preview.py` | 占位 | 本地预览 |
