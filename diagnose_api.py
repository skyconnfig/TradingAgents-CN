#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""诊断 API 和数据库问题"""

import requests
import json
from pymongo import MongoClient

MONGODB_HOST = "localhost"
MONGODB_PORT = 27017
MONGODB_DATABASE = "tradingagents"
BASE_URL = "http://localhost:8000"

def check_database():
    """检查数据库中的数据"""
    print("=" * 60)
    print("🔍 检查 MongoDB 数据库")
    print("=" * 60)
    
    try:
        client = MongoClient(f"mongodb://{MONGODB_HOST}:{MONGODB_PORT}/")
        db = client[MONGODB_DATABASE]
        
        # 检查股票基础信息
        stocks_count = db['stocks'].count_documents({})
        print(f"\n📊 stocks 集合: {stocks_count} 条记录")
        
        # 检查 000001
        stock_000001 = db['stocks'].find_one({"symbol": "000001"})
        if stock_000001:
            print(f"✅ 找到 000001: {stock_000001.get('name', 'N/A')}")
        else:
            print(f"❌ 未找到 000001")
        
        # 检查历史数据
        daily_count = db['stock_daily_data'].count_documents({"symbol": "000001"})
        print(f"\n📈 stock_daily_data 集合 (000001): {daily_count} 条记录")
        
        if daily_count > 0:
            # 显示最新一条
            latest = db['stock_daily_data'].find_one(
                {"symbol": "000001"},
                sort=[("date", -1)]
            )
            print(f"   最新数据: {latest.get('date')} - 收盘价: {latest.get('close')}")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ 数据库检查失败: {e}")
        return False

def test_api_endpoints():
    """测试各个 API 端点"""
    print("\n" + "=" * 60)
    print("🧪 测试 API 端点")
    print("=" * 60)
    
    endpoints = [
        ("健康检查", "GET", "/api/health"),
        ("股票列表", "GET", "/api/stocks?market=CN&limit=5"),
        ("股票详情", "GET", "/api/stocks/000001"),
        ("历史数据", "GET", "/api/stocks/000001/historical?days=30"),
    ]
    
    for name, method, path in endpoints:
        print(f"\n📡 测试: {name} ({method} {path})")
        try:
            url = f"{BASE_URL}{path}"
            if method == "GET":
                response = requests.get(url, timeout=10)
            else:
                response = requests.post(url, timeout=10)
            
            print(f"   状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ 成功")
                # 显示部分响应
                if isinstance(data, dict):
                    if 'total' in data:
                        print(f"   总数: {data.get('total')}")
                    if 'data' in data:
                        print(f"   数据条数: {len(data.get('data', []))}")
                elif isinstance(data, list):
                    print(f"   返回列表长度: {len(data)}")
            elif response.status_code == 404:
                print(f"   ❌ 404 - 端点不存在或数据未找到")
            elif response.status_code == 401:
                print(f"   ⚠️  需要认证")
            else:
                print(f"   ❌ 失败: {response.text[:200]}")
                
        except requests.exceptions.Timeout:
            print(f"   ⏱️ 超时")
        except Exception as e:
            print(f"   ❌ 错误: {e}")

def main():
    print("\n" + "🔍" * 30)
    print("TradingAgents-CN 诊断工具")
    print("🔍" * 30 + "\n")
    
    # 1. 检查数据库
    db_ok = check_database()
    
    # 2. 测试 API
    test_api_endpoints()
    
    print("\n" + "=" * 60)
    print("📊 诊断完成")
    print("=" * 60)

if __name__ == "__main__":
    main()
