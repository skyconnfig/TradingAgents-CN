#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
强制修复脚本
用途：将 stock_daily_data 的数据强制同步到 stock_daily_quotes
解决：分析服务读取集合不一致的问题
"""

from pymongo import MongoClient
from datetime import datetime
import time

MONGODB_HOST = "localhost"
MONGODB_PORT = 27017
MONGODB_DATABASE = "tradingagents"

print("=" * 70)
print("TradingAgents-CN 强制数据修复")
print("=" * 70)

client = MongoClient(f"mongodb://{MONGODB_HOST}:{MONGODB_PORT}/")
db = client[MONGODB_DATABASE]

source_coll = db['stock_daily_data']
target_coll = db['stock_daily_quotes']

# 1. 检查源数据
print("\n1. 检查源数据 (stock_daily_data)...")
cursor = source_coll.find({"symbol": "000001"})
records = list(cursor)
print(f"   源数据: 找到 {len(records)} 条记录")

if not records:
    print("   ❌ 严重错误：源数据为空！请先运行 direct_sync_stock_data.py")
    exit(1)

# 2. 清理目标集合（解决索引冲突的最快方法）
print("\n2. 重置目标集合 (stock_daily_quotes)...")
try:
    # 删除集合，彻底清除旧索引和坏数据
    db.drop_collection('stock_daily_quotes') 
    print("   ✅ 旧集合已删除")
except Exception as e:
    print(f"   ⚠️ 删除集合时警告 (可能不存在): {e}")

# 3. 转换并写入数据
print("\n3. 写入数据...")
new_records = []
for record in records:
    # 构造符合 HistoricalDataService 规范的文档
    new_doc = {
        "symbol": record["symbol"],
        "code": record["symbol"],
        # 生成规范的 full_symbol
        "full_symbol": f"{record['symbol']}.SZ" if record['symbol'].startswith(('0', '3')) else f"{record['symbol']}.SH",
        "market": "CN",
        "trade_date": record.get("date"), # 关键：映射 date -> trade_date
        "period": "daily",
        "data_source": "akshare",  # 明确指定数据源
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "version": 1,
        # 价格数据
        "open": float(record.get("open", 0)),
        "high": float(record.get("high", 0)),
        "low": float(record.get("low", 0)),
        "close": float(record.get("close", 0)),
        "volume": float(record.get("volume", 0)),
        "amount": float(record.get("amount", 0)), # 确保是数字
        # 计算字段（可选）
        "pre_close": None, 
        "change": None,
        "pct_chg": None
    }
    new_records.append(new_doc)

if new_records:
    target_coll.insert_many(new_records)
    print(f"   ✅ 成功写入 {len(new_records)} 条记录")
else:
    print("   ❌ 没有数据需要写入")

# 4. 重建正确索引
print("\n4. 重建索引...")
try:
    # 1. 复合唯一索引（与后端代码完全一致）
    target_coll.create_index([
        ("symbol", 1),
        ("trade_date", 1),
        ("data_source", 1),
        ("period", 1)
    ], unique=True, name="symbol_date_source_period_unique")
    
    # 2. 常用查询索引
    target_coll.create_index([("symbol", 1)], name="symbol_index")
    target_coll.create_index([("trade_date", -1)], name="trade_date_index")
    
    print("   ✅ 索引重建成功")
except Exception as e:
    print(f"   ❌ 索引创建失败: {e}")

# 5. 最终验证
print("\n5. 最终验证...")
count = target_coll.count_documents({"symbol": "000001", "period": "daily"})
latest = target_coll.find_one({"symbol": "000001"}, sort=[("trade_date", -1)])

print(f"   目标集合记录数: {count}")
if latest:
    print(f"   最新数据日期: {latest.get('trade_date')}")
    print(f"   收盘价: {latest.get('close')}")
    print("   ✅ 数据验证通过！")
else:
    print("   ❌ 数据验证失败")

client.close()
print("\n" + "=" * 70)
print("修复完成！")
print("现在请刷新浏览器，重新点击分析。")
print("=" * 70)
