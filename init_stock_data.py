#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
初始化股票数据 - 同步基础信息和历史数据
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def trigger_stock_sync():
    """触发股票数据同步"""
    print("=" * 60)
    print("📊 开始同步股票数据")
    print("=" * 60)
    
    # 1. 同步股票基础信息
    print("\n1️⃣ 同步股票基础信息...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/sync/stocks/basics",
            json={"force": True},
            timeout=300  # 5分钟超时
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 基础信息同步成功")
            print(f"📝 响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print(f"⚠️  基础信息同步失败: {response.status_code}")
            print(f"📝 响应: {response.text}")
    except Exception as e:
        print(f"❌ 基础信息同步失败: {e}")
    
    # 等待一下
    print("\n⏳ 等待 5 秒...")
    time.sleep(5)
    
    # 2. 同步单只股票的历史数据（000001 平安银行）
    print("\n2️⃣ 同步股票 000001 的历史数据...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/sync/stocks/000001/historical",
            json={
                "days": 365,  # 同步1年数据
                "force": True
            },
            timeout=300
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 历史数据同步成功")
            print(f"📝 响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print(f"⚠️  历史数据同步失败: {response.status_code}")
            print(f"📝 响应: {response.text}")
    except Exception as e:
        print(f"❌ 历史数据同步失败: {e}")
    
    print("\n" + "=" * 60)
    print("✅ 数据同步完成")
    print("=" * 60)
    print("\n📝 下一步:")
    print("1. 刷新浏览器页面")
    print("2. 重新尝试分析股票 000001")

def check_stock_data():
    """检查股票数据是否存在"""
    print("\n" + "=" * 60)
    print("🔍 检查股票数据")
    print("=" * 60)
    
    try:
        # 检查股票列表
        response = requests.get(
            f"{BASE_URL}/api/stocks?market=CN&limit=10",
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            total = result.get('total', 0)
            stocks = result.get('stocks', [])
            
            print(f"\n📊 股票总数: {total}")
            
            if stocks:
                print(f"\n前 {len(stocks)} 只股票:")
                for stock in stocks[:5]:
                    print(f"  - {stock.get('symbol')}: {stock.get('name')}")
            else:
                print("\n⚠️  数据库中没有股票数据，需要同步")
                return False
            
            return True
        else:
            print(f"❌ 检查失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        return False

def main():
    """主函数"""
    print("\n" + "🚀" * 30)
    print("TradingAgents-CN 股票数据初始化")
    print("🚀" * 30 + "\n")
    
    # 先检查数据
    has_data = check_stock_data()
    
    if not has_data:
        print("\n💡 检测到数据库为空，开始同步数据...")
        trigger_stock_sync()
    else:
        print("\n✅ 数据库中已有股票数据")
        
        # 询问是否要同步 000001 的数据
        print("\n是否要同步股票 000001 的历史数据？")
        print("这将确保分析功能正常工作")
        
        # 直接同步
        print("\n开始同步...")
        trigger_stock_sync()

if __name__ == "__main__":
    main()
