#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终综合测试 - 完整的系统验证
"""

import requests
import json
from pymongo import MongoClient

BASE_URL = "http://localhost:8000"
MONGODB_HOST = "localhost"
MONGODB_PORT = 27017
MONGODB_DATABASE = "tradingagents"

print("=" * 70)
print("TradingAgents-CN 系统综合测试")
print("=" * 70)

# 1. MongoDB 测试
print("\n1. MongoDB 连接测试")
print("-" * 70)
try:
    client = MongoClient(f"mongodb://{MONGODB_HOST}:{MONGODB_PORT}/", serverSelectionTimeoutMS=5000)
    client.server_info()
    db = client[MONGODB_DATABASE]
    
    stocks_count = db['stocks'].count_documents({})
    daily_count = db['stock_daily_data'].count_documents({"symbol": "000001"})
    
    print(f"   MongoDB: 连接成功")
    print(f"   股票数量: {stocks_count}")
    print(f"   000001 历史数据: {daily_count} 条")
    
    client.close()
except Exception as e:
    print(f"   MongoDB: 连接失败 - {e}")

# 2. 后端 API 测试
print("\n2. 后端 API 健康检查")
print("-" * 70)
try:
    response = requests.get(f"{BASE_URL}/api/health", timeout=5)
    if response.status_code == 200:
        print(f"   API: 正常运行")
    else:
        print(f"   API: 异常 ({response.status_code})")
except Exception as e:
    print(f"   API: 无法连接 - {e}")

# 3. 认证测试
print("\n3. 用户认证测试")
print("-" * 70)
try:
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={"username": "admin", "password": "admin123"},
        timeout=10
    )
    if response.status_code == 200:
        token = response.json().get("data", {}).get("access_token")
        print(f"   认证: 成功")
        print(f"   Token: {token[:50]}...")
    else:
        print(f"   认证: 失败 ({response.status_code})")
        token = None
except Exception as e:
    print(f"   认证: 错误 - {e}")
    token = None

if not token:
    print("\n认证失败，无法继续测试")
    exit(1)

headers = {"Authorization": f"Bearer {token}"}

# 4. 股票数据 API 测试
print("\n4. 股票数据 API 测试")
print("-" * 70)
try:
    response = requests.get(
        f"{BASE_URL}/api/stocks/000001/quote",
        headers=headers,
        timeout=10
    )
    if response.status_code == 200:
        data = response.json().get("data", {})
        print(f"   股票行情: 成功")
        print(f"   股票名称: {data.get('name')}")
        print(f"   当前价格: {data.get('price')}")
    else:
        print(f"   股票行情: 失败 ({response.status_code})")
        print(f"   错误: {response.text[:200]}")
except Exception as e:
    print(f"   股票行情: 错误 - {e}")

# 5. 分析 API 测试
print("\n5. 分析 API 测试")
print("-" * 70)
try:
    data = {
        "symbol": "000001",
        "market": "CN",
        "analysts": ["market"],
        "research_depth": "快速",
        "parameters": {}
    }
    
    response = requests.post(
        f"{BASE_URL}/api/analysis/single",
        headers=headers,
        json=data,
        timeout=30
    )
    
    if response.status_code == 200:
        result = response.json()
        task_id = result.get("data", {}).get("task_id")
        print(f"   分析任务: 创建成功")
        print(f"   Task ID: {task_id}")
        
        # 简单等待几秒
        import time
        print(f"   等待 5 秒...")
        time.sleep(5)
        
        # 检查状态
        status_response = requests.get(
            f"{BASE_URL}/api/analysis/tasks/{task_id}/status",
            headers=headers,
            timeout=10
        )
        
        if status_response.status_code == 200:
            status_data = status_response.json().get("data", {})
            print(f"   任务状态: {status_data.get('status')}")
            print(f"   进度: {status_data.get('progress', 0)}%")
        else:
            print(f"   状态查询: 失败 ({status_response.status_code})")
    else:
        print(f"   分析任务: 失败 ({response.status_code})")
        print(f"   错误: {response.text[:500]}")
except Exception as e:
    print(f"   分析任务: 错误 - {e}")

print("\n" + "=" * 70)
print("测试完成")
print("=" * 70)
