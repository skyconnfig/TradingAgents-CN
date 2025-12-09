#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""简化的诊断脚本 - 检查 API 问题"""

import requests
import json

BASE_URL = "http://localhost:8000"

print("=" * 60)
print("API Diagnostic Tool")
print("=" * 60)

# 测试关键端点
endpoints = {
    "Health Check": "/api/health",
    "Stock List": "/api/stocks?market=CN&limit=5",
    "Stock 000001 Info": "/api/stocks/000001",
    "Stock 000001 Historical": "/api/stocks/000001/historical?days=30",
}

for name, path in endpoints.items():
    print(f"\nTesting: {name}")
    print(f"URL: {BASE_URL}{path}")
    
    try:
        response = requests.get(f"{BASE_URL}{path}", timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"Response: {json.dumps(data, indent=2, ensure_ascii=False)[:500]}")
            except:
                print(f"Response (text): {response.text[:200]}")
        else:
            print(f"Error: {response.text[:200]}")
            
    except Exception as e:
        print(f"Exception: {e}")

print("\n" + "=" * 60)
print("Diagnostic Complete")
print("=" * 60)
