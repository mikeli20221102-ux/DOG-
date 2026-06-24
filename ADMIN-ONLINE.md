# 线上后台搭建指南 — 让运营远程改图片 / 价格 / 视频

> 目标：运营在**任何电脑**打开 `https://silkroadpaws.com/admin/`，用 **GitHub 账号登录**，
> 改图片、价格、视频，点 **Publish 直接上线**（不碰代码、不用 deploy.bat）。
>
> 用的是 **Sveltia CMS**（界面和原来一样）+ 一个免费的 **Cloudflare 登录小程序**。
> 全程免费。下面 4 步只需做一次。

---

## 准备：运营要有一个 GitHub 账号

1. 让运营到 [github.com](https://github.com) 免费注册一个账号，把**用户名**给你
2. 你打开仓库 [github.com/mikeli20221102-ux/DOG-](https://github.com/mikeli20221102-ux/DOG-)
   → **Settings → Collaborators → Add people** → 输入运营的用户名邀请
3. 运营在邮箱/GitHub 通知里点 **Accept** 接受邀请

> 没有这一步，运营登录后无法保存修改。

---

## 第 1 步：一键部署登录小程序（Cloudflare Worker）

1. 用你的 Cloudflare 账号，点这个按钮开始部署：
   **https://deploy.workers.cloudflare.com/?url=https://github.com/sveltia/sveltia-cms-auth**
2. 按提示点 **Deploy**（它会在你账户里创建一个叫 `sveltia-cms-auth` 的 Worker）
3. 部署完成后，会显示一个网址，形如：
   ```
   https://sveltia-cms-auth.你的名字.workers.dev
   ```
   **把这个网址复制下来**（第 2、4 步都要用）

---

## 第 2 步：在 GitHub 注册一个 OAuth App

1. 打开 [github.com/settings/applications/new](https://github.com/settings/applications/new)
2. 填写：
   - **Application name**：`Pawsport CMS`（随便取）
   - **Homepage URL**：`https://silkroadpaws.com`
   - **Authorization callback URL**：把第 1 步的网址加上 `/callback`，例如：
     ```
     https://sveltia-cms-auth.你的名字.workers.dev/callback
     ```
3. 点 **Register application**
4. 在出现的页面：
   - 记下 **Client ID**
   - 点 **Generate a new client secret** → 记下 **Client Secret**（只显示一次，务必复制）

---

## 第 3 步：把两串码填进 Worker

1. 回到 Cloudflare → **Workers & Pages** → 点 `sveltia-cms-auth`
2. **Settings → Variables and Secrets**（变量）→ 添加 3 个：
   | 变量名 | 值 |
   |--------|-----|
   | `GITHUB_CLIENT_ID` | 第 2 步的 Client ID |
   | `GITHUB_CLIENT_SECRET` | 第 2 步的 Client Secret（点 Encrypt 加密） |
   | `ALLOWED_DOMAINS` | `silkroadpaws.com, *.silkroadpaws.com` |
3. **Save / Deploy** 保存

---

## 第 4 步：把 Worker 网址发给我（我来收尾）

把第 1 步的 Worker 网址发给我，我会：
- 填进 `admin/config.yml` 的 `base_url`
- 推送上线

之后访问 **https://silkroadpaws.com/admin/** → 点 **Sign in with GitHub** → 就能用了。

> 你也可以自己改：打开 `admin/config.yml`，把 `base_url: https://CHANGE-ME.workers.dev`
> 换成你的 Worker 网址，保存后双击 `deploy.bat`。

---

## 运营日常怎么用（搭好之后）

1. 打开 **https://silkroadpaws.com/admin/**
2. 点 **Sign in with GitHub** 登录
3. 改内容：
   - **犬种管理**：改价格（起价）、上传/更换图片、新增品种
   - **站点设置**：邮箱、WhatsApp、数据条
   - **客户评价**：增删改
   - **视频**：见下方
4. 点 **Publish / Save** → 自动上线，1–2 分钟生效

### 视频怎么传（重要）
视频**不传后台**（太大）。流程：
1. 把视频传到 **YouTube**（可设为「不公开 Unlisted」）
2. 复制视频链接（如 `https://youtu.be/abc123`）
3. 后台「视频」→「视频链接」粘贴进去 → Publish

---

## 常见问题

**Q：运营登录后保存失败 / 看不到内容？**
多半是没把运营加成仓库 Collaborator（见「准备」第 2 步），或运营没接受邀请。

**Q：点登录卡住 / 报错？**
检查第 2 步的 callback 网址是否 = Worker 网址 + `/callback`；第 3 步三个变量是否填对、已保存。

**Q：图片太大传不上？**
后台图片请压缩到 2MB 内（用 [tinypng.com](https://tinypng.com)），单文件不要超过 25MB。

**Q：我自己电脑想改，不想登录？**
取消 `admin/config.yml` 里 `local_backend: true` 的注释，双击 `admin-local.bat` 用本地后台。
