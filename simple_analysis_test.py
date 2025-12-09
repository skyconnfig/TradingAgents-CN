#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""简化的分析测试 - 只测试能否创建任务"""

import requests
import json

BASE_URL = "http://localhost:8000"

# Login
response = requests.post(f"{BASE_URL}/api/auth/login", json={"username": "admin", "password": "admin123"})
token = response.json()["data"]["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Test analysis
data = {
    "symbol": "000001",
    "market": "CN",
    "analysts": ["market"],
}

print("Creating analysis task...")
response = requests.post(f"{BASE_URL}/api/analysis/tasks", headers=headers, json=data, timeout=30)

print(f"Status Code: {response.status_code}")
print(f"Response:")
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
