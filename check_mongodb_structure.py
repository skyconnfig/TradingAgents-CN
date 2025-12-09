#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查 MongoDB 中的数据结构"""

from pymongo import MongoClient
import json

MONGODB_HOST = "localhost"
MONGODB_PORT = 27017
MONGODB_DATABASE = "tradingagents"

client = MongoClient(f"mongodb://{MONGODB_HOST}:{MONGODB_PORT}/")
db = client[MONGODB_DATABASE]

print("=" * 60)
print("MongoDB 数据结构检查")
print("=" * 60)

# 1. 检查所有集合
print("\n1. 所有集合:")
collections = db.list_collection_names()
for coll in collections:
    count = db[coll].count_documents({})
    print(f"   - {coll}: {count} 条记录")

# 2. 检查 stock_daily_data 的数据结构
print("\n2. stock_daily_data 集合中 000001 的数据样本:")
sample = db['stock_daily_data'].find_one({"symbol": "000001"})
if sample:
    print(json.dumps(sample, indent=2, default=str, ensure_ascii=False))
else:
    print("   未找到数据")

# 3. 检查其他可能的历史数据集合
print("\n3. 检查其他可能的历史数据集合:")
possible_collections = [
    'stock_historical_data',
    'historical_data',
    'daily_data',
    'kline_data',
    'stock_data'
]

for coll_name in possible_collections:
    if coll_name in collections:
        count = db[coll_name].count_documents({"symbol": "000001"})
        print(f"   - {coll_name}: {count} 条 000001 的记录")
        if count > 0:
            sample = db[coll_name].find_one({"symbol": "000001"})
            print(f"     样本: {json.dumps(sample, indent=2, default=str, ensure_ascii=False)[:500]}")

client.close()
