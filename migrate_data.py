#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据迁移与修复脚本
将 stock_daily_data 的数据迁移到 stock_daily_quotes，以满足 HistoricalDataService 的需求
"""

from pymongo import MongoClient
import pandas as pd
from datetime import datetime

MONGODB_HOST = "localhost"
MONGODB_PORT = 27017
MONGODB_DATABASE = "tradingagents"

print("=" * 70)
print("TradingAgents-CN 数据迁移脚本: stock_daily_data -> stock_daily_quotes")
print("=" * 70)

client = MongoClient(f"mongodb://{MONGODB_HOST}:{MONGODB_PORT}/")
db = client[MONGODB_DATABASE]

source_coll = db['stock_daily_data']
target_coll = db['stock_daily_quotes']

# 1. 获取源数据
print("\n1. 读取源数据 (stock_daily_data)...")
cursor = source_coll.find({"symbol": "000001"})
records = list(cursor)
print(f"   找到 {len(records)} 条记录")

if not records:
    print("   ❌ 源集合中没有数据！请先运行 direct_sync_stock_data.py")
    exit(1)

# 2. 转换并写入目标集合
print("\n2. 转换并迁移数据 (stock_daily_quotes)...")
migrated_count = 0

for record in records:
    # 转换字段
    new_record = {
        "symbol": record["symbol"],
        "code": record["symbol"],
        "full_symbol": f"{record['symbol']}.SZ", # 假设是SZ，简单处理
        "market": "CN",
        "trade_date": record.get("date"), # 关键变换：date -> trade_date
        "period": "daily",
        "data_source": record.get("source", "akshare"),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "version": 1,
        "open": record.get("open"),
        "high": record.get("high"),
        "low": record.get("low"),
        "close": record.get("close"),
        "volume": record.get("volume"),
        "amount": record.get("amount")
    }
    
    # 唯一键：symbol + trade_date + data_source + period
    filter_doc = {
        "symbol": new_record["symbol"],
        "trade_date": new_record["trade_date"],
        "data_source": new_record["data_source"],
        "period": new_record["period"]
    }
    
    target_coll.replace_one(filter_doc, new_record, upsert=True)
    migrated_count += 1

print(f"   ✅ 成功迁移 {migrated_count} 条记录")

# 3. 验证迁移结果
print("\n3. 验证结果...")
count = target_coll.count_documents({"symbol": "000001", "period": "daily"})
print(f"   stock_daily_quotes 中 000001 的记录数: {count}")

latest = target_coll.find_one(
    {"symbol": "000001", "period": "daily"},
    sort=[("trade_date", -1)]
)
if latest:
    print(f"   最新数据日期: {latest['trade_date']}")
    print(f"   收盘价: {latest['close']}")

# 4. 创建必要的索引
print("\n4. 确保索引存在...")
target_coll.create_index([
    ("symbol", 1),
    ("trade_date", 1),
    ("data_source", 1),
    ("period", 1)
], unique=True)
print("   ✅ 索引已创建")

client.close()
print("\n" + "=" * 70)
print("数据迁移完成！请重新尝试分析。")
print("=" * 70)
