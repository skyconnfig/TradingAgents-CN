#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用 AKShare 直接同步股票数据到 MongoDB
"""

import sys
sys.path.insert(0, '.')

from pymongo import MongoClient
import akshare as ak
from datetime import datetime, timedelta
import pandas as pd

# MongoDB 连接
MONGODB_HOST = "localhost"
MONGODB_PORT = 27017
MONGODB_DATABASE = "tradingagents"

def sync_stock_basics():
    """同步股票基础信息"""
    print("=" * 60)
    print("📊 同步股票基础信息（使用 AKShare）")
    print("=" * 60)
    
    try:
        # 连接 MongoDB
        client = MongoClient(f"mongodb://{MONGODB_HOST}:{MONGODB_PORT}/")
        db = client[MONGODB_DATABASE]
        collection = db['stocks']
        
        print("\n🔍 获取 A 股股票列表...")
        # 获取 A 股股票列表
        stock_info = ak.stock_info_a_code_name()
        
        print(f"✅ 获取到 {len(stock_info)} 只股票")
        
        # 转换并插入数据
        print("\n💾 写入数据库...")
        count = 0
        for _, row in stock_info.iterrows():
            stock_data = {
                "symbol": row['code'],
                "name": row['name'],
                "market": "CN",
                "exchange": "SH" if row['code'].startswith('6') else "SZ",
                "updated_at": datetime.utcnow(),
                "source": "akshare"
            }
            
            # 更新或插入
            collection.update_one(
                {"symbol": row['code']},
                {"$set": stock_data},
                upsert=True
            )
            count += 1
            
            if count % 100 == 0:
                print(f"  已处理 {count} 只股票...")
        
        print(f"\n✅ 成功同步 {count} 只股票基础信息")
        return True
        
    except Exception as e:
        print(f"❌ 同步失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        try:
            client.close()
        except:
            pass

def sync_stock_historical(symbol="000001", days=365):
    """同步单只股票的历史数据"""
    print("\n" + "=" * 60)
    print(f"📈 同步股票 {symbol} 的历史数据")
    print("=" * 60)
    
    try:
        # 连接 MongoDB
        client = MongoClient(f"mongodb://{MONGODB_HOST}:{MONGODB_PORT}/")
        db = client[MONGODB_DATABASE]
        collection = db['stock_daily_data']
        
        # 计算日期范围
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        start_str = start_date.strftime("%Y%m%d")
        end_str = end_date.strftime("%Y%m%d")
        
        print(f"\n🔍 获取历史数据: {start_str} ~ {end_str}")
        
        # 获取历史数据
        df = ak.stock_zh_a_hist(
            symbol=symbol,
            period="daily",
            start_date=start_str,
            end_date=end_str,
            adjust="qfq"  # 前复权
        )
        
        print(f"✅ 获取到 {len(df)} 条历史数据")
        
        if len(df) == 0:
            print("⚠️  没有获取到数据")
            return False
        
        # 转换并插入数据
        print("\n💾 写入数据库...")
        count = 0
        for _, row in df.iterrows():
            data = {
                "symbol": symbol,
                "date": pd.to_datetime(row['日期']).strftime("%Y-%m-%d"),
                "open": float(row['开盘']),
                "high": float(row['最高']),
                "low": float(row['最低']),
                "close": float(row['收盘']),
                "volume": float(row['成交量']),
                "amount": float(row['成交额']),
                "updated_at": datetime.utcnow(),
                "source": "akshare"
            }
            
            # 更新或插入
            collection.update_one(
                {"symbol": symbol, "date": data['date']},
                {"$set": data},
                upsert=True
            )
            count += 1
        
        print(f"✅ 成功同步 {count} 条历史数据")
        
        # 显示最近5条数据
        print(f"\n📊 最近 5 条数据:")
        for _, row in df.tail(5).iterrows():
            print(f"  {row['日期']}: 开盘={row['开盘']}, 收盘={row['收盘']}, 成交量={row['成交量']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 同步失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        try:
            client.close()
        except:
            pass

def main():
    """主函数"""
    print("\n" + "🚀" * 30)
    print("TradingAgents-CN 股票数据直接同步")
    print("🚀" * 30 + "\n")
    
    # 1. 同步基础信息
    success1 = sync_stock_basics()
    
    # 2. 同步 000001 的历史数据
    success2 = sync_stock_historical("000001", days=365)
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 同步总结")
    print("=" * 60)
    print(f"基础信息同步: {'✅ 成功' if success1 else '❌ 失败'}")
    print(f"历史数据同步: {'✅ 成功' if success2 else '❌ 失败'}")
    
    if success1 and success2:
        print("\n🎉 数据同步完成！")
        print("\n📝 下一步:")
        print("1. 刷新浏览器页面: http://localhost:3000")
        print("2. 重新尝试分析股票 000001")
    else:
        print("\n⚠️  部分数据同步失败，请检查错误信息")

if __name__ == "__main__":
    main()
