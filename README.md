# Pawsport — B2C 独立站（静态版）

面向海外个人买家（韩国 / 东南亚 / 中东等）的高端中国犬种预订站。
**不接在线支付**：访客提交询单 → 视频看狗 → 线下定金 + 合同成交（符合"线下收费"要求）。

## 目录结构

```
pawsport-site/
├── index.html            # 单页站点
├── admin/                # Decap CMS 后台（/admin 登录管理）
│   ├── index.html
│   └── config.yml
├── content/              # ★ 网站内容数据（后台改的就是这些 JSON）
│   ├── breeds.json       # 犬种、价格、图片、介绍
│   ├── videos.json
│   ├── testimonials.json
│   └── settings.json     # 联系方式、数据条、首页图
├── assets/
│   ├── css/styles.css
│   └── js/
│       ├── i18n.js       # 界面多语言（9 种）
│       └── main.js       # 从 content/*.json 加载并渲染
├── netlify.toml          # 旧 Netlify 配置，Cloudflare 会忽略，可保留
├── DEPLOY.md             # ★ 部署上线步骤（Cloudflare Pages + silkroadpaws.com）
├── CMS-SETUP.md          # ★ 后台改内容的 3 种方式
└── README.md
```

## 后台管理（Decap CMS）

**改价格、传图片、上新品种** → 见 **`CMS-SETUP.md`**，不用改代码。

站点托管在 **Cloudflare Pages**（正式域名 https://silkroadpaws.com）。
日常改内容推荐：**本地后台** `npx decap-server`，或直接在 **GitHub 网页**改 `content/*.json`。

## 多语言

右上角语言下拉可切换，首次访问按浏览器语言自动选择，选择会记忆（localStorage）。
已内置 9 种语言：**English / 简体中文 / 한국어 / 日本語 / ภาษาไทย / Tiếng Việt /
Bahasa Indonesia / العربية（自动右到左 RTL）/ Русский**。

- 改文案：编辑 `assets/js/i18n.js`，每种语言一个对象，键名与 `index.html` 里的
  `data-i18n="..."` 一一对应。
- 加语言：在 `i18n.js` 顶部 `LANGS` 增加 `{ code, name }`，再补一个 `I18N.<code> = {...}`
  翻译对象即可；如为从右到左语言，把 code 加进 `RTL_LANGS`。
- 品种的标签/描述也分语言，键为 `breed.<key>.tag` / `breed.<key>.desc`。

## 多语言 SEO

`i18n.js` 会自动处理多语言搜索引擎收录：

- **标题 / 描述**：每种语言有 `meta.title` 与 `meta.description`，切换语言时
  `<title>`、`<meta description>`、Open Graph、Twitter 卡片标签同步更新。
- **hreflang**：自动向 `<head>` 注入 `<link rel="alternate" hreflang="...">`（含
  `x-default`），告诉 Google 各语言版本的对应关系。
- **`?lang=` 链接**：切换语言时地址栏会带上 `?lang=ko` 等参数，便于分享与抓取；
  `canonical` 也随之指向对应语言 URL。
- **正式域名**：已在 `index.html` 的 `<head>` 固定为正式地址，canonical/hreflang
  会基于它生成：

```html
<meta name="site-url" content="https://silkroadpaws.com/" />
```

## 本地预览

任选其一，在 `pawsport-site/` 目录下运行：

```bash
python -m http.server 8080
# 然后浏览器打开 http://localhost:8080
```

或用 VS Code 的 Live Server 插件直接打开 `index.html`。

## 需要你替换的内容（重要）

1. **联系方式 / 收件**：编辑 `assets/js/main.js` 顶部 `CONFIG`：
   - `whatsapp`：国际格式纯数字（如 `8210xxxxxxxx`）
   - `email`：你的接单邮箱
   - `formEndpoint`：到 [formspree.io](https://formspree.io) 免费注册拿一个表单地址填入，询单就会发到你邮箱；
     **留空或不改**则点击"发送"会自动打开访客邮件客户端（也能用）。
2. **图片 / 视频（直接放文件即可，无需改代码）**：
   - 图片放进 `assets/img/`，视频放进 `assets/video/`，**文件名按约定**（见
     `assets/img/README.txt` 与 `assets/video/README.txt`）。
   - 例如：`crested-1.jpg`（品种图）、`crested-cover.jpg`（视频封面）、
     `crested.mp4`（视频）、`hero.jpg`（首页大图）、`delivery.jpg`（交付图）。
   - 放入真实文件前，网站会**自动显示占位狗图**，不会破图；放入后自动覆盖。
   - 视频卡片：有对应封面图 + mp4 时，点击即可播放；只放封面也能正常上线。
   - 真实照片/视频是信任与转化的核心，**务必替换**。
3. **品种**：在 `BREEDS` 数组增删品种、改文案与"from $价格"。
4. **文案/品牌**：站点为英文（面向海外买家）。品牌名 `Pawsport` 可在 `index.html` 与样式中替换。

## 部署

**当前线上：Cloudflare Pages + 域名 `silkroadpaws.com` —— 完整步骤见 `DEPLOY.md`。**

纯静态，无需构建命令，连 GitHub 自动部署、避免 ICP 备案。更新只需 `git push`（或双击 `deploy.bat`）。

## 合规与支付提醒

- **不要接 Shopify / Stripe / PayPal 标准支付**销售活体；本站刻意只做询单 + 线下成交。
- 交付外包给正规出境托运代办 + flight nanny / IPATA 会员（白手套押运）。
- 各目的国进口规则（芯片 / 狂犬疫苗 / 抗体滴度 / 许可 / 检疫）需逐国满足；
  加拿大等国禁止从中国商业进口犬只——下单前先确认买家所在国可行。
