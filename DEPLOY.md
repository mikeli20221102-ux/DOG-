# 部署上线指南 — Cloudflare Pages + silkroadpaws.com

> 正式域名：**https://silkroadpaws.com**
> 托管：**Cloudflare Pages**（免费、不限流量、自带 CDN + HTTPS）
> 代码仓库：**GitHub `mikeli20221102-ux/DOG-`**
> 更新方式：改完 `git push` → Cloudflare 自动重新部署

---

## 第一步：把最新代码推到 GitHub

在 `pawsport-site` 目录运行（或双击 `deploy.bat`）：

```bash
git add -A
git commit -m "switch to silkroadpaws.com + cloudflare"
git push
```

确认仓库根目录有：`index.html`、`admin/`、`content/`、`assets/`、`breeds/`、`guide/`、`markets/`、`sitemap.xml`、`robots.txt`。

---

## 第二步：Cloudflare Pages 连接 GitHub（约 5 分钟）

1. 登录 [dash.cloudflare.com](https://dash.cloudflare.com)
2. 左侧 **Workers & Pages** → **Create** → **Pages** → **Connect to Git**
3. 授权并选择仓库：`mikeli20221102-ux/DOG-`
4. 构建设置：
   - **Framework preset**：`None`
   - **Build command**：留空
   - **Build output directory**：`.`（一个点，表示仓库根目录）
5. 点 **Save and Deploy**
6. 部署完成后会得到一个临时地址，如 `https://dog-xxx.pages.dev` —— 先打开确认网站正常

> 说明：`netlify.toml` 在 Cloudflare 上会被忽略，不影响运行，可保留。

---

## 第三步：绑定自定义域名 silkroadpaws.com

### 情况 A：域名就在 Cloudflare 注册（最简单）

1. 进入刚创建的 Pages 项目 → **Custom domains** → **Set up a custom domain**
2. 输入 `silkroadpaws.com` → 按提示确认
3. 再加一个 `www.silkroadpaws.com`（可选，Cloudflare 会自动加 DNS 记录）
4. 等待状态变为 **Active**（通常几分钟，HTTPS 证书自动签发）

### 情况 B：域名在别处注册（Namecheap 等）

1. 先把域名的 **Nameservers（DNS 服务器）** 改成 Cloudflare 提供的两条
   （Cloudflare 控制台 **Add a site** 会给你），等生效
2. 再按情况 A 绑定

完成后访问 **https://silkroadpaws.com** 应能打开网站。

---

## 第四步：上线后验证清单

- [ ] https://silkroadpaws.com 首页正常、图片正常
- [ ] https://silkroadpaws.com/sitemap.xml 能打开（17 条 URL）
- [ ] https://silkroadpaws.com/guide/index.html 指南页正常
- [ ] https://silkroadpaws.com/breeds/chow-chow.html 品种页正常
- [ ] 切换语言时地址栏出现 `?lang=ko` 等，canonical 跟随变化
- [ ] 询单表单能正常发送（Formspree 收件）

---

## 以后怎么更新网站

改完文件后，任选其一：

- **双击 `deploy.bat`**（自动 add / commit / push）
- 或手动 `git add -A && git commit -m "..." && git push`
- 或直接在 **GitHub 网页**编辑 `content/*.json` 后 Commit

推送后 **1–2 分钟** Cloudflare 自动上线，无需手动操作。

---

## 第五步：把站点地图提交给 Google

1. 打开 [Google Search Console](https://search.google.com/search-console)
2. 添加资源（域名 `silkroadpaws.com`，按提示做 DNS 验证）
3. 左侧 **站点地图** → 提交：

```
https://silkroadpaws.com/sitemap.xml
```

---

## 后台 `/admin` 怎么办？

迁到 Cloudflare 后，原来的 Netlify 邮箱登录**不能用了**。
日常改价格/图片/品种，见 **`CMS-SETUP.md`**，推荐：

- **本地后台**：`npx decap-server` + 打开 `localhost:8080/admin/`（最简单，开箱即用）
- 或 **GitHub 网页**直接改 `content/*.json`
- 想要线上可视化后台 → 接 **GitHub OAuth 登录**（CMS-SETUP.md 第四节）
