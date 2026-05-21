# PersonWebsite

> 个人站点：简历 + 写作（EP 系列），静态构建，发布到 GitHub Pages。

---

## GitHub 仓库

| 项目 | 地址 | 说明 |
|------|------|------|
| **PersonWebsite** | https://github.com/wuyaorui2001-crypto/PersonWebsite | 本站源码与构建产物 |
| **thoughts** | https://github.com/wuyaorui2001-crypto/thoughts | EP 文章写作主库（同步来源） |

### 恢复方法

```bash
git clone https://github.com/wuyaorui2001-crypto/PersonWebsite.git
cd PersonWebsite
cat SYSTEM.md
```

**线上地址**（仓库创建并部署后）：https://wuyaorui2001-crypto.github.io/PersonWebsite/

---

## 本地路径

`D:\Me&AI\Project\PersonWebsite`

---

## 日常维护（站长）

改内容 → `git push` → GitHub Actions 构建 `docs/` → GitHub Pages 更新。  
分场景步骤与检查清单见 **[`PRD.md` 第六节 §6.4](PRD.md#64-发布到线上日常维护必记)**。

---

## 快速开始

### 1. 投放简历 PDF

将简历 PDF 放到：

```
content/source/resume.pdf
```

然后由 Agent 运行（或自行执行）：

```bash
python scripts/extract_resume.py
```

生成对照文本；**网站展示**请编辑 `content/resume.md`（上中文 / 下 English，见 PRD 6.1）。

### 2. 同步文章（EP 系列）

```bash
python scripts/sync_articles.py
python scripts/build.py
```

从 `D:\Me&AI\Project\thoughts\Article\` 拉取 `EP 00x` 到 `content/articles/`，再构建 `docs/`。

### 3. 本地预览

```bash
python scripts/preview.py
```

浏览器打开 `http://127.0.0.1:8080/PersonWebsite/`（需先 build）。

### 4. 发布线上

按 [`PRD.md` §6.4](PRD.md#64-发布到线上日常维护必记)：`git push` → GitHub Actions 部署 Pages。  
**首次上线**步骤见 [`DEPLOY.md`](DEPLOY.md)。

---

## 目录结构

```
PersonWebsite/
├── config/sections.yaml    # 板块注册（可扩展）
├── content/
│   ├── source/resume.pdf   # 你投放的简历原件
│   ├── resume.md           # 简历主文档（上中文 / 下 English）
│   ├── articles/           # EP 文章副本 + manifest.json
│   └── work-retrospective/ # 未来：工作复盘
├── site/                   # 模板与样式（frontend-design）
├── scripts/                # 抽取 / 同步 / 构建 / 压测
└── docs/                   # 构建产物（Pages 根目录）
```

---

## PRD-first

**所有功能变更先改 [`PRD.md`](PRD.md)（产品可读版，非纯研发文档），再改代码。**  
简历：仅 `content/resume.md`（上中文 / 下 English）；简历页中英切换见 PRD 6.1.2。

## 状态

| 阶段 | 状态 |
|------|------|
| P1 脚手架 | 完成 |
| P1b 简历 | 完成（`resume.md` 初稿；正式工作后顶部追加经历） |
| PRD v0.2 | 完成 |
| P2 视觉设计 | 待开始 |
| P3–P5 构建与部署 | 待开始 |
