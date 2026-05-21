# 简历原件目录

请将你的简历 PDF 放在此目录，文件名为：

```
resume.pdf
```

完整路径：

```
D:\Me&AI\Project\PersonWebsite\content\source\resume.pdf
```

放好后运行：

```bash
cd D:\Me&AI\Project\PersonWebsite
python scripts/extract_resume.py
```

脚本生成 `resume_extracted.txt`；**请对照更新** `content/resume.md`（网站展示源）。

入职正式工作后：在 `resume.md` 里中英文两段的 `工作经历` / `Work Experience` 一起写（可删掉「沉淀中」/ In progress）。详见 `PRD.md` 第六节。

**说明**：若 PDF 含隐私信息且不想提交 Git，可在项目根 `.gitignore` 中取消注释 `content/source/resume.pdf`。
