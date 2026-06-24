@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo.
echo ========================================
echo  Pawsport - 一键更新网站 (推送到 GitHub)
echo ========================================
echo.
echo Cloudflare Pages 已连接 GitHub：push 后会自动重新部署。
echo 正式域名：https://silkroadpaws.com
echo.

git add -A
set /p msg="输入本次修改说明 (直接回车用默认): "
if "%msg%"=="" set msg=update site content
git commit -m "%msg%"
git push

echo.
if %ERRORLEVEL% EQU 0 (
  echo 已推送！1-2 分钟后 Cloudflare 会自动上线，刷新 https://silkroadpaws.com 查看。
) else (
  echo 推送失败。请检查 git 是否已配置远程仓库，或先运行： git push -u origin main
)
echo.
pause
