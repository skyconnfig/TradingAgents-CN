#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的后端启动脚本，用于调试
"""

import sys
import traceback

try:
    print("🚀 开始启动 TradingAgents 后端...")
    print("📍 Python 版本:", sys.version)
    print("📍 工作目录:", sys.path[0])
    
    print("\n1️⃣ 导入 FastAPI...")
    from fastapi import FastAPI
    
    print("2️⃣ 导入 uvicorn...")
    import uvicorn
    
    print("3️⃣ 导入 app.main...")
    from app.main import app
    
    print("4️⃣ 启动服务...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
    
except Exception as e:
    print(f"\n❌ 启动失败！")
    print(f"错误类型: {type(e).__name__}")
    print(f"错误信息: {e}")
    print("\n完整错误堆栈:")
    traceback.print_exc()
    sys.exit(1)
