#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试分析 API"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

print("=" * 60)
print("Test Analysis API")
print("=" * 60)

# Step 1: Login
print("\n1. Login...")
login_data = {"username": "admin", "password": "admin123"}

try:
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data, timeout=10)
    if response.status_code == 200:
        token = response.json().get("data", {}).get("access_token")
        print(f"   Token: {token[:50]}...")
    else:
        print(f"   ERROR: {response.text}")
        exit(1)
except Exception as e:
    print(f"   ERROR: {e}")
    exit(1)

headers = {"Authorization": f"Bearer {token}"}

# Step 2: Test Analysis API
print("\n2. Test Analysis API...")
print("-" * 60)

# 创建分析任务
analysis_data = {
    "symbol": "000001",
    "market": "CN",
    "analysts": ["market", "fundamental"],  # 市场分析师和基本面分析师
    "config": {
        "deep_think_llm": "deepseek-chat",
        "quick_think_llm": "deepseek-chat"
    }
}

print(f"\nRequest: POST /api/analysis/tasks")
print(f"Data: {json.dumps(analysis_data, indent=2, ensure_ascii=False)}")

try:
    response = requests.post(
        f"{BASE_URL}/api/analysis/tasks",
        headers=headers,
        json=analysis_data,
        timeout=30
    )
    
    print(f"\nStatus: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)[:500]}")
    
    if response.status_code == 200:
        result = response.json()
        task_id = result.get("data", {}).get("task_id")
        if task_id:
            print(f"\nTask ID: {task_id}")
            print("\nWaiting for analysis to complete...")
            
            # 轮询任务状态
            for i in range(30):  # 最多等待30秒
                time.sleep(1)
                status_response = requests.get(
                    f"{BASE_URL}/api/analysis/tasks/{task_id}",
                    headers=headers,
                    timeout=10
                )
                
                if status_response.status_code == 200:
                    status_data = status_response.json().get("data", {})
                    status = status_data.get("status")
                    print(f"   [{i+1}s] Status: {status}")
                    
                    if status == "completed":
                        print("\nAnalysis completed!")
                        print(f"Result: {json.dumps(status_data, indent=2, ensure_ascii=False)[:500]}")
                        break
                    elif status == "failed":
                        print(f"\nAnalysis failed!")
                        print(f"Error: {status_data.get('error')}")
                        break
    else:
        print(f"\nERROR: {response.text}")
        
except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
