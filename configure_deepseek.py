#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""通过 API 配置 DeepSeek"""

import requests
import json

# API 基础地址
BASE_URL = "http://localhost:8000"

# DeepSeek 配置
deepseek_config = {
    "provider": "deepseek",
    "model_name": "deepseek-chat",
    "api_key": "sk-08090b8782904fc09cee9da664a187c2",
    "base_url": "https://api.deepseek.com",
    "enabled": True,
    "is_default": True,
    "model_type": "chat",
    "supports_vision": False,
    "supports_function_calling": True,
    "max_tokens": 4096,
    "temperature": 0.7
}

try:
    # 尝试获取当前配置
    print("🔍 检查 API 服务状态...")
    response = requests.get(f"{BASE_URL}/api/health", timeout=5)
    print(f"✅ API 服务正常: {response.json()}")
    
    # 配置 DeepSeek
    print("\n🔧 正在配置 DeepSeek...")
    # 注意：这里需要根据实际的 API 端点调整
    # 可能需要先登录获取 token
    
    print("\n📝 DeepSeek 配置信息:")
    print(json.dumps(deepseek_config, indent=2, ensure_ascii=False))
    
    print("\n⚠️  请在 Web 界面手动配置:")
    print("1. 访问: http://localhost:3000")
    print("2. 进入 '设置' -> '配置管理' -> 'LLM 配置'")
    print("3. 添加 DeepSeek 配置:")
    print(f"   - Provider: deepseek")
    print(f"   - Model: deepseek-chat")
    print(f"   - API Key: sk-08090b8782904fc09cee9da664a187c2")
    print(f"   - Base URL: https://api.deepseek.com")
    print(f"   - 启用: ✓")
    
except requests.exceptions.ConnectionError:
    print("❌ 无法连接到 API 服务")
    print("请确保后端服务正在运行: http://localhost:8000")
except Exception as e:
    print(f"❌ 错误: {e}")
