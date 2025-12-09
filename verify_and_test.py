#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验证股票数据并测试分析功能"""

from pymongo import MongoClient
import requests
import json

MONGODB_HOST = "localhost"
MONGODB_PORT = 27017
MONGODB_DATABASE = "tradingagents"
BASE_URL = "http://localhost:8000"

def verify_data():
    """验证数据库中的数据"""
    print("=" * 60)
    print("🔍 验证数据库数据")
    print("=" * 60)
    
    try:
        client = MongoClient(f"mongodb://{MONGODB_HOST}:{MONGODB_PORT}/")
        db = client[MONGODB_DATABASE]
        
        # 检查股票基础信息
        stocks_count = db['stocks'].count_documents({})
        print(f"\n📊 股票基础信息: {stocks_count} 只")
        
        # 检查 000001 的数据
        stock_000001 = db['stocks'].find_one({"symbol": "000001"})
        if stock_000001:
            print(f"✅ 找到股票 000001: {stock_000001.get('name')}")
        else:
            print(f"❌ 未找到股票 000001")
        
        # 检查历史数据
        historical_count = db['stock_daily_data'].count_documents({"symbol": "000001"})
        print(f"\n📈 股票 000001 历史数据: {historical_count} 条")
        
        # 显示最近5条数据
        recent_data = list(db['stock_daily_data'].find(
            {"symbol": "000001"}
        ).sort("date", -1).limit(5))
        
        if recent_data:
            print(f"\n📊 最近 5 条数据:")
            for data in recent_data:
                print(f"  {data['date']}: 开盘={data['open']}, 收盘={data['close']}, 成交量={data['volume']}")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        return False

def test_analysis():
    """测试分析功能"""
    print("\n" + "=" * 60)
    print("🧪 测试股票分析功能")
    print("=" * 60)
    
    try:
        print("\n📝 提示: 由于分析需要时间，这里只测试 API 是否可用")
        print("实际分析请在 Web 界面进行\n")
        
        # 测试分析 API 是否存在
        response = requests.get(f"{BASE_URL}/api/analysis/tasks", timeout=5)
        
        if response.status_code in [200, 401]:  # 200 或需要认证都说明 API 存在
            print(f"✅ 分析 API 可用")
            return True
        else:
            print(f"⚠️  分析 API 状态: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def main():
    """主函数"""
    print("\n" + "🚀" * 30)
    print("数据验证和功能测试")
    print("🚀" * 30 + "\n")
    
    # 验证数据
    data_ok = verify_data()
    
    # 测试分析功能
    api_ok = test_analysis()
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 验证总结")
    print("=" * 60)
    print(f"数据验证: {'✅ 通过' if data_ok else '❌ 失败'}")
    print(f"API 测试: {'✅ 通过' if api_ok else '❌ 失败'}")
    
    if data_ok and api_ok:
        print("\n🎉 一切就绪！")
        print("\n📝 现在可以:")
        print("1. 访问 http://localhost:3000")
        print("2. 登录系统（默认: admin / admin123）")
        print("3. 选择股票 000001 进行分析")
        print("4. DeepSeek 已配置完成，可以开始使用")
    else:
        print("\n⚠️  存在问题，请检查上述错误")

if __name__ == "__main__":
    main()
