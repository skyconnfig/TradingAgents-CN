#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""模拟前端请求，测试分析 API"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

# 1. 登录
print("1. 登录...")
response = requests.post(
    f"{BASE_URL}/api/auth/login",
    json={"username": "admin", "password": "admin123"}
)
token = response.json()["data"]["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# 2. 提交分析请求（模拟前端的完整请求）
print("\n2. 提交分析请求...")
request_data = {
    "symbol": "000001",
    "stock_code": "000001",
    "parameters": {
        "market_type": "A股",
        "analysis_date": "2025-12-08",
        "research_depth": "快速",
        "selected_analysts": ["market", "fundamental"],
        "include_sentiment": True,
        "include_risk": True,
        "language": "zh-CN",
        "quick_analysis_model": "deepseek-chat",
        "deep_analysis_model": "deepseek-chat"
    }
}

print(f"请求数据: {json.dumps(request_data, indent=2, ensure_ascii=False)}")

response = requests.post(
    f"{BASE_URL}/api/analysis/single",
    headers=headers,
    json=request_data,
    timeout=30
)

print(f"\n状态码: {response.status_code}")
print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

if response.status_code == 200:
    result = response.json()
    task_id = result.get("data", {}).get("task_id")
    
    if task_id:
        print(f"\n3. 任务 ID: {task_id}")
        print("\n4. 等待 10 秒后查询状态...")
        time.sleep(10)
        
        status_response = requests.get(
            f"{BASE_URL}/api/analysis/tasks/{task_id}/status",
            headers=headers
        )
        
        print(f"\n状态查询结果:")
        print(json.dumps(status_response.json(), indent=2, ensure_ascii=False))
