#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证 MongoDBCacheAdapter 数据读取
"""

import sys
import os
from pathlib import Path
import pandas as pd

# 添加项目根目录到路径
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

from tradingagents.dataflows.cache.mongodb_cache_adapter import get_mongodb_cache_adapter
from tradingagents.utils.stock_validator import StockDataPreparer

print("=" * 70)
print("MongoDBCacheAdapter 验证")
print("=" * 70)

adapter = get_mongodb_cache_adapter()
print(f"1. 适配器状态: use_app_cache={adapter.use_app_cache}, db={adapter.db.name if adapter.db else 'None'}")

if not adapter.use_app_cache:
    print("   ❌ 缓存未启用！")
    # 强制启用以便测试
    print("   🔄 强制初始化连接...")
    adapter._init_mongodb_connection()
    adapter.use_app_cache = True

# 1. 检查数据源优先级
print("\n2. 数据源优先级:")
priority = adapter._get_data_source_priority("000001")
print(f"   000001: {priority}")

# 2. 直接查询 stock_daily_quotes
print("\n3. 直接 MongoDB 查询:")
coll = adapter.db.stock_daily_quotes
count = coll.count_documents({"symbol": "000001", "data_source": "akshare"})
print(f"   stock_daily_quotes 中 000001 (akshare) 数量: {count}")

latest = coll.find_one({"symbol": "000001", "data_source": "akshare"}, sort=[("trade_date", -1)])
if latest:
    print(f"   最新记录: {latest.get('trade_date')} - Close: {latest.get('close')}")
else:
    print("   未找到记录")

# 3. 使用适配器查询
print("\n4. 适配器查询 (get_historical_data):")
df = adapter.get_historical_data("000001")

if df is not None and not df.empty:
    print(f"   ✅ 成功获取数据: {len(df)} 条")
    print(f"   列名: {df.columns.tolist()}")
    print(f"   最新数据:\n{df.tail(1)}")
else:
    print("   ❌ 获取失败: 返回 None 或空")

# 4. 模拟 stock_validator 的逻辑
print("\n5. 模拟 StockValidator - _check_database_data:")
preparer = StockDataPreparer()
# 手动构造日期范围（模拟最近）
from datetime import datetime, timedelta
end_date = datetime.now()
start_date = end_date - timedelta(days=365)
start_str = start_date.strftime('%Y-%m-%d')
end_str = end_date.strftime('%Y-%m-%d')

print(f"   检查范围: {start_str} -> {end_str}")
result = preparer._check_database_data("000001", start_str, end_str)
print(f"   检查结果: {result}")

print("\n" + "=" * 70)
