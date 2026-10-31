# 银发守护 · Git 一键同步脚本
# 用法：
#   .\sync.ps1                 自动生成提交说明并推送
#   .\sync.ps1 "修复了语音识别"  用指定说明提交并推送
param([string]$Message = "")

$ErrorActionPreference = "Continue"
Set-Location $PSScriptRoot

# 提交说明
if ([string]::IsNullOrWhiteSpace($Message)) {
    $Message = "chore: 同步更新 $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
}

Write-Host "=== 1/3 暂存改动 ===" -ForegroundColor Cyan
git add -A

Write-Host "=== 2/3 提交 ===" -ForegroundColor Cyan
git -c user.name="luyaning" -c user.email="3244275632@qq.com" commit -m $Message
$commitExit = $LASTEXITCODE

if ($commitExit -ne 0) {
    Write-Host "没有需要提交的改动（工作区已是最新）。" -ForegroundColor Yellow
} else {
    Write-Host "提交成功。" -ForegroundColor Green
}

Write-Host "=== 3/3 推送 ===" -ForegroundColor Cyan
$remotes = git remote
if ([string]::IsNullOrWhiteSpace($remotes)) {
    Write-Host "尚未配置远程仓库。请先执行：" -ForegroundColor Yellow
    Write-Host '  git remote add origin <你的仓库地址>' -ForegroundColor Yellow
    Write-Host '  git push -u origin main' -ForegroundColor Yellow
} else {
    git push
    if ($LASTEXITCODE -eq 0) {
        Write-Host "推送成功 ✅" -ForegroundColor Green
    } else {
        Write-Host "推送失败，检查网络或认证（GitHub 需 Token / Gitee 需账号密码）。" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "=== 当前状态 ===" -ForegroundColor Cyan
git status --short
git log --oneline -1
