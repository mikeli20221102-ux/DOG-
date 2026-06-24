# 后台管理指南（Cloudflare 版）

> 站点已迁到 **Cloudflare Pages**，正式域名 **https://silkroadpaws.com**。
> 后台用来**改价格、传图片、上新品种、改评价**，不用动代码。

⚠️ 重要：原来的 Netlify 邮箱登录（git-gateway + Identity）**离开 Netlify 后不能用了**。
下面给你 3 种在 Cloudflare 上改内容的方式，按从易到难排序。

---

## 方式一：本地后台（推荐日常使用，开箱即用）

可视化界面，和原来 `/admin` 一模一样，只是跑在你自己电脑上。

**一次性准备：** 安装 [Node.js](https://nodejs.org)（LTS 版）。

**每次改内容：**

1. 打开 `admin/config.yml`，把这一行的注释去掉：
   ```yaml
   local_backend: true
   ```
2. 在 `pawsport-site` 目录开两个终端：
   - 终端 A：`npx decap-server`
   - 终端 B：`python -m http.server 8080`
3. 浏览器打开 **http://localhost:8080/admin/**
4. 直接改价格、传图、加品种 → 点 **Publish**（会写入本地文件）
5. 改完后推送上线：双击 `deploy.bat`，或 `git add -A && git commit -m "更新内容" && git push`
6. 1–2 分钟后 https://silkroadpaws.com 自动更新

> 上线前记得把 `local_backend: true` 重新注释掉（避免线上误用）。

---

## 方式二：GitHub 网页直接改（零安装，最省事）

适合只改文字/价格的小改动。

1. 打开仓库 `https://github.com/mikeli20221102-ux/DOG-`
2. 进入 `content/` → 点要改的文件：
   - `breeds.json` — 品种、价格（`priceFrom`）、图片、介绍
   - `settings.json` — 邮箱、WhatsApp、Facebook、数据条
   - `testimonials.json` — 客户评价
   - `videos.json` — 视频
3. 点右上角铅笔 ✏️ **Edit** → 改完 → **Commit changes**
4. Cloudflare 自动重新部署，1–2 分钟生效

> 传图片：进入 `assets/img/` → **Add file → Upload files**，文件名按 `assets/img/README.txt` 约定（如 `chow-1.jpg`）。

---

## 方式三：线上可视化后台（GitHub 登录，高级）

想在任何电脑打开 `https://silkroadpaws.com/admin/` 登录改内容，需要把后台从
Netlify 登录改成 **GitHub OAuth 登录**。步骤概览：

1. GitHub → **Settings → Developer settings → OAuth Apps → New OAuth App**
   - Homepage URL：`https://silkroadpaws.com`
   - Authorization callback URL：你的 OAuth 中转地址
   - 拿到 **Client ID** 和 **Client Secret**
2. 部署一个 OAuth 中转（Cloudflare Worker / Pages Functions，用来安全地换取登录令牌）
3. 改 `admin/config.yml` 的 backend：
   ```yaml
   backend:
     name: github
     repo: mikeli20221102-ux/DOG-
     branch: main
     base_url: https://你的OAuth中转域名
   ```
4. 删除 `admin/index.html` 里的 Netlify Identity 脚本那一行
5. 推送后访问 `/admin/` → **Login with GitHub**

> 这步需要 OAuth App 的 Client ID/Secret 和一个中转服务，配置较多。
> 准备好后告诉我，我可以帮你改好 `config.yml`、`admin/index.html` 并给出 Worker 代码。

---

## 新增一个犬种（方式一/三 的可视化后台里操作）

1. **犬种管理 → 所有犬种 → 犬种列表 → Add item**
2. 填写：
   - **ID（key）**：英文小写，如 `samoyed`（创建后勿改）
   - **上架显示**：勾选
   - **英文名 / 中文名**
   - **起价 USD**（网站自动显示「起价 ～ 3 倍」区间）
   - **封面图**、**详情相册**（点 Upload 直接传图）
   - 中英文标签、介绍、体型 / 性格等
3. **Publish** → 前台自动出现新品种，询单下拉也会更新

> 若用方式二（GitHub 改 JSON），照着 `breeds.json` 里已有品种的结构，复制一段改成新品种即可。

---

## 常见问题

**Q：线上 https://silkroadpaws.com/admin/ 打开后登录失败？**
正常 —— 那是旧的 Netlify 登录。请改用上面的方式一或方式二；要线上登录走方式三。

**Q：Publish / push 后前台没变？**
等 Cloudflare 部署完成（Pages 项目 → Deployments 看状态）；浏览器强制刷新（Ctrl+F5）。

**Q：视频文件怎么传？**
把 mp4 上传到 `assets/video/`，在「视频」里填路径如 `assets/video/新品种.mp4`。

**Q：本地预览整站？**
`pawsport-site` 目录运行 `python -m http.server 8080`，打开 http://localhost:8080
