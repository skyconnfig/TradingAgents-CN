#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""完整的 API 测试 - 包括认证"""

import requests
import json

BASE_URL = "http://localhost:8000"

print("=" * 60)
print("Complete API Test with Authentication")
print("=" * 60)

# Step 1: Login
print("\nStep 1: Login")
print("-" * 60)

login_data = {
    "username": "admin",
    "password": "admin123"
}

try:
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data, timeout=10)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        token = result.get("data", {}).get("access_token")
        if token:
            print(f"Token: {token[:50]}...")
        else:
            print("ERROR: No token in response")
            print(f"Response: {json.dumps(result, indent=2, ensure_ascii=False)}")
            exit(1)
    else:
        print(f"ERROR: Login failed")
        print(f"Response: {response.text}")
        exit(1)
        
except Exception as e:
    print(f"ERROR: {e}")
    exit(1)

# Step 2: Test Stock API with token
print("\nStep 2: Test Stock API")
print("-" * 60)

headers = {
    "Authorization": f"Bearer {token}"
}

endpoints = [
    ("Stock Quote", f"/api/stocks/000001/quote"),
    ("Stock KLine", f"/api/stocks/000001/kline?period=day&limit=30"),
]

for name, path in endpoints:
    print(f"\nTesting: {name}")
    print(f"URL: {BASE_URL}{path}")
    
    try:
        response = requests.get(f"{BASE_URL}{path}", headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Success!")
            # 显示部分数据
            if "data" in data:
                if isinstance(data["data"], dict):
                    print(f"Data keys: {list(data['data'].keys())}")
                elif isinstance(data["data"], list):
                    print(f"Data count: {len(data['data'])}")
        else:
            print(f"Error: {response.text[:200]}")
            
    except Exception as e:
        print(f"Exception: {e}")

print("\n" + "=" * 60)
print("Test Complete")
print("=" * 60)
