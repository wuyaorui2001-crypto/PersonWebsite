# MEMORY - PersonWebsite

## 2026-05-21 P1 脚手架

- 创建项目目录与 `config/sections.yaml` 板块注册表
- 简历流程：`content/source/resume.pdf` → `extract_resume.py` → `content/resume.md`
- 文章：从 thoughts `Article/EP *.md` 同步；架构按 ~2000 篇分页 + 增量构建设计
- UI：P2 使用 frontend-design skill，Tone 暂定 Editorial
- GitHub 仓库与 Pages workflow：P5 待创建

## 2026-05-21 PRD + 简历可扩展

- 新增 **PRD.md**（SSOT）；工作流：先 PRD 后代码
- 新增 **`.cursor/skills/personwebsite-prd/SKILL.md`**（项目内 PRD-first skill）
- 社区 `generate-requirements` 仅作方法论参考，不全量引入
- 已从 `resume.pdf` 生成 `content/resume.md`（实习经历）；`## 工作经历` 支持入职后顶部追加正式工作
- `extract_resume.py` 输出 `resume_extracted.txt`，不自动覆盖 resume.md

## 2026-05-21 PRD v0.3 + 简历总-分

- 用户反馈：PRD 太研发化 → 重写为产品可读版（v0.3）
- 简历：按「总-分」重写，非 PDF 直贴；量化结果 **加粗**
- 美团/得物：多方向用小标题 + 总 + 分

## 2026-05-21 PRD v0.5 Agent 可读

- PRD 附录 D：Agent 维护指南（启动清单、仓库地图、任务分类、Invariant、构建常错点）
- 第一节双读者阅读顺序；skill / SYSTEM 指向附录 D；v0.5.1 去掉 § 交叉引用

## 2026-05-21 P2–P4 站点构建

- P2：`site/styles`（Editorial）、`templates/`、`resume-i18n.js`
- P3：`sync_articles.py` 同步 EP 001–003 → `content/articles/` + manifest
- P4：`build.py` 输出 `docs/`（首页、简历中英切换、文章列表/详情）
- 本地：`python scripts/sync_articles.py` → `python scripts/build.py` → `python scripts/preview.py`

## 待办

- [x] resume.pdf → resume.md 初稿
- [x] P2 site/ 视觉
- [x] P3 sync（benchmark 未跑）
- [x] P4 build.py
- [ ] P5 push + Pages（本地 git init/commit 完成；push 因网络待重试，见 DEPLOY.md）
