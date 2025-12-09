#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""正确的分析 API 测试"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

print("=" * 60)
print("Correct Analysis API Test")
print("=" * 60)

# Login
print("\n1. Login...")
response = requests.post(f"{BASE_URL}/api/auth/login", json={"username": "admin", "password": "admin123"})
token = response.json()["data"]["access_token"]
headers = {"Authorization": f"Bearer {token}"}
print(f"   Token: {token[:50]}...")

# Create analysis task
print("\n2. Create Analysis Task...")
data = {
    "symbol": "000001",
    "market": "CN",
    "analysts": ["market", "fundamental"],
    "research_depth": "快速",
    "parameters": {}
}

print(f"   Request: POST /api/analysis/single")
response = requests.post(f"{BASE_URL}/api/analysis/single", headers=headers, json=data, timeout=30)

print(f"   Status: {response.status_code}")

if response.status_code == 200:
    result = response.json()
    print(f"   Response: {json.dumps(result, indent=2, ensure_ascii=False)[:500]}")
    
    task_id = result.get("data", {}).get("task_id")
    if task_id:
        print(f"\n3. Task ID: {task_id}")
        print("\n4. Polling task status...")
        
        for i in range(60):  # 最多等待60秒
            time.sleep(1)
            status_response = requests.get(
                f"{BASE_URL}/api/analysis/tasks/{task_id}/status",
                headers=headers,
                timeout=10
            )
            
            if status_response.status_code == 200:
                status_data = status_response.json().get("data", {})
                status = status_data.get("status")
                progress = status_data.get("progress", 0)
                print(f"   [{i+1}s] Status: {status}, Progress: {progress}%")
                
                if status == "completed":
                    print("\n5. Analysis Completed!")
                    # Get result
                    result_response = requests.get(
                        f"{BASE_URL}/api/analysis/tasks/{task_id}/result",
                        headers=headers,
                        timeout=10
                    )
                    if result_response.status_code == 200:
                        result_data = result_response.json().get("data", {})
                        print(f"   Summary: {result_data.get('summary', '')[:200]}...")
                        print(f"   Recommendation: {result_data.get('recommendation', '')[:200]}...")
                    break
                elif status == "failed":
                    print(f"\n5. Analysis Failed!")
                    print(f"   Error: {status_data.get('error')}")
                    break
else:
    print(f"   ERROR: {response.text}")

print("\n" + "=" * 60)
