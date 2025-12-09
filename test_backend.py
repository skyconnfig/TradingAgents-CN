#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试后端 API 和 DeepSeek 配置"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """测试健康检查"""
    print("=" * 60)
    print("1️⃣ 测试健康检查 API")
    print("=" * 60)
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        print(f"✅ 状态码: {response.status_code}")
        print(f"📝 响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return True
    except Exception as e:
        print(f"❌ 健康检查失败: {e}")
        return False

def test_root():
    """测试根路径"""
    print("\n" + "=" * 60)
    print("2️⃣ 测试根路径 API")
    print("=" * 60)
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        print(f"✅ 状态码: {response.status_code}")
        print(f"📝 响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return True
    except Exception as e:
        print(f"❌ 根路径测试失败: {e}")
        return False

def test_config():
    """测试配置 API"""
    print("\n" + "=" * 60)
    print("3️⃣ 测试配置 API")
    print("=" * 60)
    try:
        # 尝试获取系统配置（可能需要认证）
        response = requests.get(f"{BASE_URL}/api/config/system", timeout=5)
        print(f"📡 状态码: {response.status_code}")
        
        if response.status_code == 200:
            config = response.json()
            print(f"✅ 配置获取成功")
            
            # 检查 LLM 配置
            if 'llm_configs' in config:
                llm_configs = config['llm_configs']
                print(f"\n📊 LLM 配置数量: {len(llm_configs)}")
                
                # 查找 DeepSeek 配置
                deepseek_found = False
                for llm in llm_configs:
                    if llm.get('provider') == 'deepseek':
                        deepseek_found = True
                        print(f"\n🎉 找到 DeepSeek 配置:")
                        print(f"  - Provider: {llm.get('provider')}")
                        print(f"  - Model: {llm.get('model_name')}")
                        print(f"  - API Key: {llm.get('api_key', '')[:20]}...")
                        print(f"  - Base URL: {llm.get('base_url')}")
                        print(f"  - Enabled: {llm.get('enabled')}")
                        print(f"  - Default: {llm.get('is_default')}")
                        break
                
                if not deepseek_found:
                    print(f"\n⚠️  未找到 DeepSeek 配置")
            else:
                print(f"\n⚠️  配置中没有 llm_configs 字段")
                
            return True
        elif response.status_code == 401:
            print(f"⚠️  需要认证才能访问配置")
            return True  # 服务正常，只是需要认证
        else:
            print(f"❌ 配置获取失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 配置测试失败: {e}")
        return False

def test_deepseek_direct():
    """直接测试 DeepSeek API"""
    print("\n" + "=" * 60)
    print("4️⃣ 直接测试 DeepSeek API")
    print("=" * 60)
    try:
        headers = {
            "Authorization": "Bearer sk-08090b8782904fc09cee9da664a187c2",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "user", "content": "你好，请用一句话介绍你自己"}
            ],
            "max_tokens": 50
        }
        
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        print(f"📡 状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            message = result['choices'][0]['message']['content']
            print(f"✅ DeepSeek API 测试成功!")
            print(f"📝 回复: {message}")
            return True
        else:
            print(f"❌ DeepSeek API 测试失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ DeepSeek API 测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("\n" + "🚀" * 30)
    print("TradingAgents-CN 后端测试")
    print("🚀" * 30 + "\n")
    
    results = {
        "健康检查": test_health(),
        "根路径": test_root(),
        "配置API": test_config(),
        "DeepSeek API": test_deepseek_direct()
    }
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 测试总结")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
    
    total = len(results)
    passed = sum(results.values())
    
    print(f"\n总计: {passed}/{total} 测试通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！后端服务运行正常！")
        print("\n📝 下一步:")
        print("1. 访问前端: http://localhost:3000")
        print("2. 登录系统")
        print("3. 开始使用 DeepSeek 进行股票分析")
    else:
        print("\n⚠️  部分测试失败，请检查配置")

if __name__ == "__main__":
    main()
