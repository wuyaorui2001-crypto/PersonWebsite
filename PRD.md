# PersonWebsite 产品需求文档

| 项目 | 说明 |
|------|------|
| 产品名 | PersonWebsite（个人网站） |
| 版本 | v0.5.1 |
| 更新日期 | 2026-05-21 |
| 读者 | 站长（你）+ 未来维护本项目的 Agent |
| 负责人 | 吴垚枘 |
| 线上地址 | https://wuyaorui2001-crypto.github.io/PersonWebsite/（上线后填写） |

---

## 一、这份文档是干什么的

这是**个人网站**的单一事实来源（SSOT）。读完后应能回答：

1. 网站**给谁看、解决什么**（第二至第四节）  
2. 页面上**有什么、URL 是什么**（第五节）  
3. 内容**怎么改**（第六节）  
4. **怎么发布到线上**（第六节 6.4）  
5. 加新板块**怎么走**（第六节 6.3 + 附录 D）  
6. **什么叫做完**（第七节）  

> 下文用 **「第×节」** 指本文标题（如「## 二、…」= 第二节），不用 `§` 符号，避免误读为乱码。

### 给谁读、怎么读

| 读者 | 建议阅读顺序 | 用途 |
|------|----------------|------|
| **你（站长）** | 第二节 → 第六节 → 6.4 → 第七节 | 日常改简历/文章、发布、验收 |
| **Agent** | **附录 D（必读）** → 第六节 → 第五节 → `SYSTEM.md` | 改代码/配置/构建前对齐规则，避免破坏约定 |

### 维护规则（人与 Agent 相同）

```
需求或规则变化 → 先改 PRD.md（+ 第十节变更记录）
              → 若操作步骤变了，改 SYSTEM.md
              → 再改 config / content / site / scripts
              → 本地 build（+ 用户要求时 push）
```

- **不要**只改代码不更新 PRD。  
- **不要**用 AI 改写 EP 文章或简历正文（除非用户明确要求润色）。  
- 命令与逐步 SOP：**`SYSTEM.md`**；本 PRD 写**做什么、为什么、边界**。

技术实现索引：附录 C（简表）、**附录 D（Agent 专用）**。

---

## 二、产品一句话

> 我的个人主页：展示**简历** + 已发布的 **EP 系列文章**；风格偏阅读体验，后续可扩展「工作复盘」等栏目。

---

## 三、为什么做

| 动机 | 说明 |
|------|------|
| 对外展示 | 招聘、合作、读者了解我是谁、做过什么 |
| 内容沉淀 | 文章已在 thoughts 项目写，网站负责**公开展示** |
| 自己好用 | 简历会随工作更新；文章会持续增加；站点结构要能扩展 |

---

## 四、给谁用

| 用户 | 典型场景 |
|------|----------|
| 访客（HR、同事、读者） | 看简历、读文章 |
| 我（站长） | 改简历、同步文章、以后加栏目 |
| Agent / 协作者 | 按 PRD 改需求，按 SYSTEM 执行 |

---

## 五、网站里有什么（页面结构）

访问者能打开的页面：

| 页面 | 地址示例 | 内容从哪来 |
|------|----------|------------|
| 首页 | `/` | 简短介绍 + 进入简历 / 文章的入口 |
| 简历 | `/resume/` | `content/resume.md` |
| 文章列表 | `/articles/`、`/articles/page/2/`… | 从 thoughts 同步的 EP 文章，**分页**（每页约 30 篇） |
| 文章详情 | `/articles/ep-001-答案/` | 单篇文章正文 |
| 工作复盘（未上线） | `/work-retrospective/` | 预留，见下文 |

**关于「父子页面」**：  
GitHub Pages 就是一堆网页文件，**完全可以**做成「栏目 / 子页面」结构（例如 `/work-retrospective/2026-q1/`）。不需要服务器，和常见官网一样。

---

## 六、内容怎么维护

### 6.1 简历（重点）

| 问题 | 答案 |
|------|------|
| 现在是什么 | **实习经历**已写满；**工作经历**单独一节，暂显示「沉淀中」 |
| 以后入职正式工作 | 在「工作经历」里按总-分写法补充；实习经历保留不动 |
| 日常怎么改 | **只改一个文件** `content/resume.md`：上半中文、下半 English |
| 中英切换 | 仅在**简历页**提供按钮，见 6.1.2 |
| PDF 原件 | 放在 `content/source/resume.pdf`，仅作备份或大批量对照；**网站以 MD 为准** |

#### 6.1.2 简历中英切换（简历页专属）

| 项 | 说明 |
|----|------|
| 源文件 | **仅** `content/resume.md` |
| 文件结构 | 上：`# 中文` + `<!-- RESUME_LANG:zh -->` 至技能节末；下：`<!-- RESUME_LANG:en -->` 后接 `# English` 与英文正文 |
| 维护习惯 | 新增一段实习/工作时，**紧挨着**在中英文两处各写一遍（结构对齐，方便对照） |
| 入口 | 访客打开 `/resume/` 简历页 |
| 按钮位置 | 页面固定：**右下角**（或左上/右上，实现时在 PRD 附录 C 与样式里二选一，默认右下） |
| 按钮文案 | 当前为中文时显示 **English**；当前为英文时显示 **中文**（或并排 **中文 \| English**，高亮当前语言） |
| 交互 | 点击后在同一页切换正文，不跳转新 URL；语言偏好可记入浏览器本地（可选） |
| 维护 | 同一文件内中英两段同步改；构建脚本按 `RESUME_LANG` 标记切分 |

#### 简历写法（必须遵守，不是随便贴 PDF）

每一段实习/工作采用 **「总 → 分」** 结构：

1. **总（一句）**：这一段工作的整体职责，单独一段，**不要**加 `*` 或 `-`  
   - 例：*负责优化支付宝平台商家入驻各环节流程，提升商家入驻成功率*

2. **分（多条）**：具体事项，每条一行，用 `*` 开头  
   - 例：`* 优化入驻链路数据漏斗看板：……`

3. **同一家公司多个方向**（如美团「首页消费」和「体验优化」）：  
   - 用小标题（如 `**首页消费**`）  
   - 下面再「总一句 + 多条 *」

4. **有数字的结果要加粗**：如 **2pt**、**5%**、**5.6H**、**2800**、**3 次**、**7 次** 等，方便扫读

5. **禁止**：把 PDF 逐行抄成同级 bullet；不要把「总」和「分」混在同一层级

入职后：在 **## 工作经历** 下写入（可删掉「沉淀中」）；结构仍为总-分 + 结果加粗。实习保持在 **## 实习经历**。

简历章节顺序建议：教育经历 → **工作经历** → **实习经历** → 技能。

### 6.2 文章（EP 系列）

| 问题 | 答案 |
|------|------|
| 写在哪 | thoughts 项目 `D:\Me&AI\Project\thoughts\Article\`，文件名 `EP 001 标题.md` |
| 网站怎么用 | `python scripts/sync_articles.py` → 复制到 `content/articles/{slug}.md` |
| 会不会改我原文 | **不会**。同步为复制；构建不调用 AI 改文 |
| URL 规则 | 文件名 `EP 001 答案.md` → slug `ep-001-答案` → `/articles/ep-001-答案/` |
| 很多篇怎么办 | 列表分页（每页 30，见 `config/sections.yaml`）；架构按约 **2000 篇** 预留 |
| CI 注意 | GitHub Actions **没有** thoughts 仓库；**必须把** `content/articles/*.md` 提交进 PersonWebsite，线上才显示新文章 |

### 6.3 工作复盘（预留）

- 打算以后写「工作复盘」类内容  
- 现在**不做**，只在规划里留位置  
- 上线时要：改 PRD、打开配置、新建内容文件夹、做列表和详情页

### 6.4 发布到线上（日常维护，必记）

网站不是「改仓库里的 Markdown 就自动变成网页」，而是：**本地改源文件 → 推到 GitHub → 云端自动构建 → GitHub Pages 展示构建结果**。

#### 一句话链路

```
本地改 content/（+ 文章时先同步 thoughts）
    → git commit & push 到 PersonWebsite 仓库
    → GitHub Actions 自动跑 build.py，生成 docs/
    → 部署到 GitHub Pages（公网可访问）
```

#### 分场景怎么做

| 我改了什么 | 本地要做什么 | 推送到 GitHub 后 |
|------------|--------------|------------------|
| 只改简历文字 | 编辑 `content/resume.md`（中英两段一起改） | Actions 构建 → 简历页更新 |
| 换了简历 PDF 对照 | 放 `content/source/resume.pdf`，需要时用抽取脚本生成对照文本，再**手工**合并进 `resume.md` | 同上 |
| 发了新 EP / 改了文章 | 在 thoughts 写好 → 运行同步脚本更新 `content/articles/` | Actions 构建 → 列表/详情页更新 |
| 想先看效果再推 | 本地运行 `build.py`，用 `preview.py` 预览（可选） | 不 push 则线上不变 |

#### 和「仓库」「Pages」的关系

| 对象 | 是什么 | 你要不要常改 |
|------|--------|--------------|
| **GitHub 仓库** | 源码：Markdown、配置、模板、脚本 | ✅ 日常改这里 |
| **`docs/` 文件夹** | 构建出的 HTML/CSS/JS（访客看到的网页） | ❌ 一般不用手改；由 `build.py` 生成 |
| **GitHub Pages** | 托管 `docs/` 里的静态站 | ❌ 不用单独操作；push 触发 Actions 后自动更新 |

**常见误解**：不是「把整个仓库原样挂上网」，而是 **push 触发自动化构建，只发布 `docs/`**。

#### 发布检查（push 之后）

1. 打开仓库 **Actions**，确认最近一次 **Deploy PersonWebsite** 为绿色成功。  
2. 打开线上地址（如 `https://wuyaorui2001-crypto.github.io/PersonWebsite/`），刷新简历页或文章页核对。  
3. 若 Actions 失败：看日志（多为 `build.py` 报错或依赖问题），修好后再 push 一次。

#### 本地预览（可选，上线前推荐）

- 目的：不 push 也能在浏览器里看「构建后的站」，避免把错误推到公网。  
- 步骤：`python scripts/build.py` → `python scripts/preview.py`（P4 完成后可用）。  
- **推送到 GitHub 后，云端会再构建一遍**；本地预览通过 ≠ 线上一定成功，但以 Actions 绿勾为准。

#### 维护习惯（和 PRD-first 一起记）

| 顺序 | 做什么 |
|------|--------|
| 1 | 需求/结构变了 → **先改 PRD**（含本节与第六节内容规则） |
| 2 | 改 `content/` 或同步文章 |
| 3 | 可选本地 build + 预览 |
| 4 | `git push` → 等 Actions → 打开公网链接验收 |

技术命令与逐步 SOP 见 **`SYSTEM.md`**。Agent 场景对照表见 **附录 D 的 D.3**。

---

## 七、做成什么样算满意（验收标准）

### 第一期（当前目标）

- [ ] 打开网站能看到**好看**的首页、简历页、文章列表和文章页（视觉单独用设计规范，见附录 B）  
- [ ] 简历结构与 `content/resume.md` 一致：**总-分**、结果数字加粗  
- [ ] 简历页可切换 **中文 / English**，从同一 `resume.md` 切出两段渲染  
- [ ] 3 篇 EP 文章能读，列表能翻页（为大量文章预留）  
- [ ] 我能在 MD 里改简历、同步文章，无需改代码  
- [ ] 推送到 GitHub 后，公网链接能访问  

### 暂不做的

- 登录、评论、后台管理系统  
- 全站搜索（以后再说）  
- 同步 thoughts 里所有笔记（只要 EP 系列）

---

## 八、版本规划（路线图）

| 阶段 | 交付物 | 状态 |
|------|--------|------|
| P1 项目骨架 | 文件夹、PRD、配置 | 已完成 |
| P1b 简历内容 | `resume.md` 按总-分写好 | 已完成 |
| P2 页面视觉 | 首页 / 简历 / 文章 好看 | 已完成（Editorial） |
| P3 文章同步 | 从 thoughts 拉 EP + 大量文章压测 | 已完成（3 篇）；压测未做 |
| P4 生成网页 | 本地能预览完整站 | 已完成 |
| P5 上线 | GitHub 仓库 + 公网链接 | 进行中（本地已 commit，待 push + Pages） |

---

## 九、改需求时怎么走

**站长 / Agent 共用流程：**

```
有新想法
  → 判断：只改正文？还是改规则/结构/页面？（见附录 D 的 D.3）
  → 若改规则/结构：更新 PRD 对应章节 + 第十节变更记录 + 版本号
  → 若 SOP/命令变化：更新 SYSTEM.md
  → 实现（config / content / site / scripts）
  → python scripts/build.py（文章变更前先 sync_articles.py）
  → 用户要求发布时：git push → 等 Actions 绿勾 → 验收第六节 6.4
```

**Agent 额外约束**（细则在附录 D）：

- 进入本项目先读：`.cursor/skills/personwebsite-prd/SKILL.md`  
- **禁止**在未更新 PRD 的情况下新增路由、板块、改简历文件结构  
- **禁止**提交 `content/source/resume.pdf`（已在 `.gitignore`）

---

## 十、变更记录

| 版本 | 日期 | 改了什么 |
|------|------|----------|
| v0.1 | 2026-05-21 | 初版 |
| v0.2 | 2026-05-21 | 增加 PRD-first、简历可扩展 |
| v0.3 | 2026-05-21 | 全文改为产品可读表述；明确简历「总-分」结构与结果加粗规则 |
| v0.3.1 | 2026-05-21 | 简历拆为「工作经历（沉淀中）」+「实习经历」两节 |
| v0.4 | 2026-05-21 | 简历页中英切换按钮（PRD 6.1.2） |
| v0.4.1 | 2026-05-21 | 中英合并为单文件 `resume.md`（删除 resume.en.md） |
| v0.4.2 | 2026-05-21 | 新增 6.4「发布到线上」日常维护链路 |
| v0.5 | 2026-05-21 | 新增附录 D「Agent 维护指南」；双读者说明；6.2 CI 与 slug 规则 |
| v0.5.1 | 2026-05-21 | 交叉引用改为「第×节」，去掉 § 符号 |

---

## 附录 A：关联内容仓库

| 名称 | 用途 |
|------|------|
| PersonWebsite | 本网站项目 |
| thoughts | 文章写作（EP 系列） |
| agent-workspace | Agent 工作记忆（可选） |

---

## 附录 B：视觉与阅读（给设计和研发）

- 整体要**好看**，避免千篇一律的「AI 模板站」  
- 风格方向：**杂志 /  editorial**，适合长文  
- 文章正文参考 thoughts 排版习惯：字号约 15px、行距舒适、深灰字  
- 改版时主要动「样式和模板」，**不要改**文章和简历原文  

---

## 附录 C：研发实现摘要

| 项 | 说明 |
|----|------|
| 本地目录 | `D:\Me&AI\Project\PersonWebsite` |
| 板块配置 | `config/sections.yaml`（`enabled` / `path` / `template`） |
| 构建输出 | `docs/` → GitHub Pages；**勿手改** `docs/`，改 `site/` 或 `content/` 后重新 build |
| 构建脚本 | `scripts/build.py`（读 yaml + resume 切分 + 文章 manifest/ glob） |
| 同步脚本 | `scripts/sync_articles.py`（源：`thoughts/Article/EP *.md`） |
| PDF | `extract_resume.py` → `resume_extracted.txt` only；**不覆盖** `resume.md` |
| 预览 | `scripts/preview.py` → `http://127.0.0.1:8080/PersonWebsite/` |
| 部署 | `.github/workflows/pages.yml`；首次 push 见 `DEPLOY.md` |
| Agent 细则 | **附录 D**；逐步命令 **`SYSTEM.md`** |

---

## 附录 D：Agent 维护指南（必读）

> 本节给 **Cursor / 其他 Agent**：用表格和路径减少猜测；与第六节、第九节、`SYSTEM.md`、`.cursor/skills/personwebsite-prd/SKILL.md` 一致。

### D.1 启动清单（每次接任务先执行）

1. 读 **PRD.md**（本文件）相关章节 + **附录 D 的 D.3** 判断任务类型。  
2. 读 **`SYSTEM.md`** 对应场景（A–E）。  
3. 读 **`config/sections.yaml`** 确认板块是否 `enabled`。  
4. 若改 UI：读 **frontend-design** skill，Tone = **Editorial**（见附录 B）。  
5. 改完后：`python scripts/build.py`；若动文章则先 `sync_articles.py`。  
6. 更新 **`MEMORY.md`** 简短记录（用户未禁止时）。  
7. **仅当用户明确要求** 时 `git commit` / `git push`。

### D.2 仓库地图（SSOT 与路径）

| 路径 | 类型 | 谁维护 | 说明 |
|------|------|--------|------|
| `PRD.md` | SSOT 产品 | 人 + Agent | 规则变必须先改 |
| `SYSTEM.md` | SOP | Agent 为主 | 命令与步骤 |
| `config/sections.yaml` | 配置 | Agent | 板块注册；与第五节 URL 一致 |
| `content/resume.md` | 内容 | 人为主 | 简历展示源；中英单文件 |
| `content/articles/*.md` | 内容 | sync 生成 | 从 thoughts 复制，需提交仓库 |
| `content/source/resume.pdf` | 私有输入 | 人 | **gitignore**，不 push |
| `site/templates/` | 模板 | Agent | HTML 骨架 |
| `site/styles/` | 样式 | Agent | 改版主要改这里 |
| `site/assets/scripts/resume-i18n.js` | 脚本 | Agent | 简历中英切换 |
| `scripts/build.py` | 构建 | Agent | 生成 `docs/` |
| `scripts/sync_articles.py` | 同步 | Agent | 拉 EP 文章 |
| `docs/` | 构建产物 | build 生成 | CI 与本地 build 产出 |
| `.cursor/skills/personwebsite-prd/` | Agent skill | Agent | PRD-first 流程 |

### D.3 任务分类 → 必须动作

| 用户意图 / 任务 | 先改 PRD？ | 主要改动 | 必跑命令 |
|-----------------|------------|----------|----------|
| 只改简历文字（无结构变化） | 否 | `content/resume.md` 中英两段 | `build.py` |
| 简历增删章节、改中英结构 | **是** 第六节 6.1 | `resume.md` + 可能 `build.py` | `build.py` |
| 新 EP / 改文章 | 否 | thoughts 原文 → sync | `sync_articles.py` → `build.py` |
| 改分页、新板块、新 URL | **是** 第五节、6.3 | `sections.yaml` + 模板 + `build.py` | `build.py` |
| 改视觉、排版 | 视情况 附录 B | `site/styles/`、`site/templates/` | `build.py` |
| 发布线上 | 否 | — | 用户 `git push`；验 Actions |
| 换 PDF 对照 | 否 | `content/source/resume.pdf` | `extract_resume.py`；**手工**合并进 MD |

### D.4 不可违反的约定（Invariant）

| # | 规则 |
|---|------|
| 1 | 简历展示源 **仅** `content/resume.md`；须含 `<!-- RESUME_LANG:zh -->` 与 `<!-- RESUME_LANG:en -->` |
| 2 | 简历经历：**总述一句（无 bullet）+ 多条 `*` 分述**；数字结果 **加粗** |
| 3 | `## 工作经历` 与 `## 实习经历` **分开**；暂无正式工作时中文「沉淀中」/ 英文 `In progress` |
| 4 | 同步文章 **不修改** Markdown 正文；只复制文件 |
| 5 | EP slug：`EP {n} {标题}.md` → `ep-{n:03d}-{标题无空格小写}`，例 `ep-001-答案` |
| 6 | `base_url` 固定为 `/PersonWebsite/`（`sections.yaml`），所有站内链接需带此前缀 |
| 7 | **不提交** `resume.pdf`；**不**让 build 用 AI 重写简历/文章 |
| 8 | 新增板块：PRD 第五节、第六节 + `sections.yaml` `enabled: true` + `content/<板块>/` + 模板 |

### D.5 简历文件结构（供解析）

```text
---
YAML frontmatter（name, headline, updated, changelog…）
---
# 中文
# 姓名
联系方式
<!-- RESUME_LANG:zh -->
## 教育经历
…
## 技能
…
<!-- RESUME_LANG:en -->
# English
# Name
contact
## Education
…
```

- `build.py` 在 marker 处切分；去掉 `# 中文` / `# English` 标题行后转 HTML。  
- 改 UI 切换按钮：模板 `site/templates/resume.html` + `config/sections.yaml` 的 `i18n_*` 字段。

### D.6 构建与部署（Agent 常错点）

| 误解 | 事实 |
|------|------|
| push Markdown 即上网 | push 触发 **Actions** 跑 `build.py`，发布 **`docs/`** |
| CI 会 sync thoughts | **不会**；须本地 `sync_articles.py` 后 **commit** `content/articles/` |
| 改 `docs/*.html` 即可 | 下次 build **覆盖**；应改 `site/` 或 `content/` |
| 预览路径根目录 | 本地：`http://127.0.0.1:8080/PersonWebsite/`（含 base_url） |

### D.7 验收时对照第七节

Agent 完成 UI/构建类任务后，核对：

- [ ] 首页、简历（中英切换）、文章列表、至少 1 篇详情可访问  
- [ ] 简历 HTML 符合总-分；加粗数字保留  
- [ ] `build.py` 退出码 0；无破坏 `RESUME_LANG` marker  
- [ ] 若用户要上线：提醒第六节 6.4 / `DEPLOY.md`，不擅自 force push  

### D.8 与 `personwebsite-prd` skill 的关系

- **PRD（本文件）**：产品与规则 SSOT，含附录 D。  
- **skill**：强制「先 PRD 后代码」的执行顺序与检查清单。  
- **SYSTEM.md**：可复制粘贴的命令级 SOP。  

三者冲突时：**PRD > SYSTEM > skill 示例**；有歧义时问用户并更新第十节变更记录。
