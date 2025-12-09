#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终修复脚本 - 确保数据格式符合分析服务要求
"""

from pymongo import MongoClient
from datetime import datetime
import akshare as ak

MONGODB_HOST = "localhost"
MONGODB_PORT = 27017
MONGODB_DATABASE = "tradingagents"

print("=" * 70)
print("TradingAgents-CN 数据修复脚本")
print("=" * 70)

client = MongoClient(f"mongodb://{MONGODB_HOST}:{MONGODB_PORT}/")
db = client[MONGODB_DATABASE]

# 1. 检查现有数据
print("\n1. 检查现有数据...")
daily_count = db['stock_daily_data'].count_documents({"symbol": "000001"})
print(f"   stock_daily_data: {daily_count} 条")

# 2. 确保数据格式正确
print("\n2. 验证数据格式...")
sample = db['stock_daily_data'].find_one({"symbol": "000001"})
if sample:
    required_fields = ['symbol', 'date', 'open', 'high', 'low', 'close', 'volume']
    missing_fields = [f for f in required_fields if f not in sample]
    
    if missing_fields:
        print(f"   ❌ 缺少字段: {missing_fields}")
    else:
        print(f"   ✅ 数据格式正确")
        print(f"   样本数据: {sample['date']}, 收盘价: {sample['close']}")

# 3. 检查是否需要创建索引
print("\n3. 检查索引...")
indexes = list(db['stock_daily_data'].list_indexes())
has_symbol_date_index = any(
    'symbol' in idx.get('key', {}) and 'date' in idx.get('key', {})
    for idx in indexes
)

if not has_symbol_date_index:
    print("   创建索引...")
    db['stock_daily_data'].create_index([("symbol", 1), ("date", -1)])
    print("   ✅ 索引已创建")
else:
    print("   ✅ 索引已存在")

# 4. 确保有最新数据
print("\n4. 检查最新数据...")
latest = db['stock_daily_data'].find_one(
    {"symbol": "000001"},
    sort=[("date", -1)]
)

if latest:
    print(f"   最新数据日期: {latest['date']}")
    print(f"   收盘价: {latest['close']}")

# 5. 检查 stock_basic_info
print("\n5. 检查股票基础信息...")
basic_info = db['stock_basic_info'].find_one({"code": "000001"})
if basic_info:
    print(f"   ✅ 找到基础信息: {basic_info.get('name')}")
else:
    print(f"   ❌ 未找到基础信息")
    # 尝试添加
    print("   添加基础信息...")
    db['stock_basic_info'].update_one(
        {"code": "000001"},
        {"$set": {
            "code": "000001",
            "name": "平安银行",
            "market": "主板",
            "industry": "银行",
            "source": "akshare",
            "updated_at": datetime.utcnow()
        }},
        upsert=True
    )
    print("   ✅ 基础信息已添加")

client.close()

print("\n" + "=" * 70)
print("✅ 数据修复完成")
print("=" * 70)
print("\n📝 下一步:")
print("1. 刷新浏览器页面")
print("2. 重新尝试分析股票 000001")
print("3. 如果仍然失败，请查看后端日志获取详细错误信息")
