# P5 上线清单

## 1. 推送代码（本地已完成 init + commit）

```powershell
cd "D:\Me&AI\Project\PersonWebsite"
git remote -v   # 应为 origin → github.com/.../PersonWebsite.git
git push -u origin main
```

若网络失败，可稍后重试，或改用 SSH：

```powershell
git remote set-url origin git@github.com:wuyaorui2001-crypto/PersonWebsite.git
git push -u origin main
```

## 2. GitHub 上创建仓库（若尚未创建）

1. 打开 https://github.com/new  
2. Repository name：`PersonWebsite`  
3. **不要**勾选 “Add a README”（本地已有）  
4. 创建后执行上面的 `git push`

## 3. 启用 GitHub Pages

1. 仓库 → **Settings** → **Pages**  
2. **Build and deployment** → Source 选 **GitHub Actions**（不是 “Deploy from a branch”）  
3. 首次 push 后，**Actions** 页应出现 **Deploy PersonWebsite** workflow

## 4. 验收

- Actions 全部为绿色  
- 访问：https://wuyaorui2001-crypto.github.io/PersonWebsite/  
- 简历中英切换、3 篇 EP 文章可打开  

## 5. 隐私说明

`content/source/resume.pdf` 已在 `.gitignore`，不会进入公开仓库；线上以 `content/resume.md` 为准。
