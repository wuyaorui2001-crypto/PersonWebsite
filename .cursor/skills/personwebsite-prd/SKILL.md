---
name: personwebsite-prd
description: PersonWebsite 项目 PRD-first 工作流。任何功能、结构、简历格式、文章规则、板块扩展、构建或部署变更，必须先更新 PRD.md 再改代码。在 PersonWebsite 目录下工作时自动适用。
---

# PersonWebsite PRD-first

## 何时使用

在 `PersonWebsite` 项目内做任何**非纯文案**变更时：

- 新增/修改板块（如工作复盘）
- 改简历结构、同步规则、文章分页策略
- 改构建脚本、GitHub Pages、目录结构
- 改 `site/` 信息架构或路由

**不适用**：仅修改 `content/resume.md` 正文文字、单篇 EP 原文（无规则变化）。

## 强制顺序

```
1. 阅读 PRD.md（项目根）— Agent 必读附录 D
2. 用 PRD 附录 D 的 D.3 判断任务类型（是否要先改 PRD）
3. 确认变更属于哪一章 → 更新 PRD.md + 第十节变更记录 + 版本号
4. 若 SOP 变化 → 更新 SYSTEM.md
5. 实现代码 / config / content 结构
6. 更新 MEMORY.md（完成复盘）
7. sync（若文章）→ build.py；用户要求时 push
```

## PRD 位置

- **SSOT**：[`PRD.md`](../../PRD.md) — 站长第一至七节；**Agent 必读附录 D**
- **操作指南**：[`SYSTEM.md`](../../SYSTEM.md)
- **板块注册**：[`config/sections.yaml`](../../config/sections.yaml)

## 简历规则（摘自 PRD 第六节，禁止照搬 PDF）

- 展示源：`content/resume.md`
- **总-分结构**：每段经历先写**一句总述**（无 bullet），再写多条 `*` 分述
- 同公司多方向：用 `**小标题**` + 总述 + `*` 分述（参考美团、得物）
- **量化结果加粗**：2pt、5%、5.6H、2800、次数等
- 禁止把总述和分述都写成同级 `-` 列表
- `## 工作经历`：正式工作；暂无内容时写「沉淀中」
- `## 实习经历`：实习内容，与工作经历分开
- 中英：同一 `resume.md`，`RESUME_LANG:zh` / `RESUME_LANG:en` 两段；新增经历时中英一起改
- 发布：PRD 第六节 6.4 — 本地改 content → push → Actions build → Pages；细节命令见 SYSTEM.md
- PDF 仅作对照：`extract_resume.py` → `resume_extracted.txt`，需理解结构后写入 MD

## 与外部 PRD skill 的关系

- **本 skill**：维护**本项目** PRD 与实现一致，轻量、仓库内嵌
- **generate-requirements**（社区）：适合大型新功能多文档产出；本项目**不默认调用**，仅借鉴「Truth over completeness、先需求后实现」原则

## 检查清单（每次改功能前）

- [ ] 已读 PRD **附录 D 的 D.3**，确认任务分类
- [ ] PRD.md 已更新版本与第十节变更记录（若改规则/结构）
- [ ] 验收可对照 PRD 第七节 + 附录 D 的 D.7
- [ ] `sections.yaml` 与 PRD 第五节一致
- [ ] 未在 PRD 未记录的情况下新增路由或板块
- [ ] 新 EP 已 sync 且 `content/articles/*.md` 将随 commit 提交（CI 无 thoughts）
