
Write-Host "正在停止 TradingAgents 后端服务..."
$port = 8000
$tcp = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue

if ($tcp) {
    $p = $tcp.OwningProcess
    Write-Host "发现进程 ID: $p 正在监听端口 $port"
    Stop-Process -Id $p -Force
    Write-Host "进程已终止"
} else {
    Write-Host "端口 $port 没有被占用"
}

Write-Host "正在启动新的后台服务..."
$env:PYTHONPATH = "."
# 显式设置环境变量，确保生效
$env:MONGODB_ENABLED = "true"
$env:TA_USE_APP_CACHE = "true"

& .venv\Scripts\python.exe app\main.py
