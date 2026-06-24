@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ========================================
echo  Pawsport 本地后台（上传图片 / 改内容）
echo ========================================
echo.
echo 需要先装好 Node.js (https://nodejs.org) 和 Python。
echo 正在启动，请勿关闭弹出的两个黑窗口...
echo.

start "Pawsport-CMS" cmd /k "npx decap-server"
timeout /t 4 >nul
start "Pawsport-WEB" cmd /k "python -m http.server 8080"
timeout /t 3 >nul
start "" http://localhost:8080/admin/

echo.
echo 后台已在浏览器打开： http://localhost:8080/admin/
echo 改完 / 传完图后，回到项目双击 deploy.bat 推送上线。
echo （用完可关闭那两个黑窗口）
echo.
pause
