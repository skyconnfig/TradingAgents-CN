#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接通过 MongoDB 配置 DeepSeek API Key
"""

from pymongo import MongoClient
from datetime import datetime
import sys

# MongoDB 连接配置
MONGODB_HOST = "localhost"
MONGODB_PORT = 27017
MONGODB_DATABASE = "tradingagents"

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
    "temperature": 0.7,
    "created_at": datetime.utcnow(),
    "updated_at": datetime.utcnow()
}

try:
    print("🔌 正在连接 MongoDB...")
    # 不使用认证连接
    client = MongoClient(f"mongodb://{MONGODB_HOST}:{MONGODB_PORT}/", serverSelectionTimeoutMS=5000)
    
    # 测试连接
    client.server_info()
    print("✅ MongoDB 连接成功")
    
    # 选择数据库
    db = client[MONGODB_DATABASE]
    
    # 查找或创建配置集合
    config_collection = db['system_config']
    
    # 查找现有配置
    existing_config = config_collection.find_one({})
    
    if existing_config:
        print("📝 找到现有配置，正在更新...")
        # 更新 LLM 配置
        if 'llm_configs' not in existing_config:
            existing_config['llm_configs'] = []
        
        # 检查是否已有 DeepSeek 配置
        deepseek_exists = False
        for i, llm in enumerate(existing_config['llm_configs']):
            if llm.get('provider') == 'deepseek':
                existing_config['llm_configs'][i] = deepseek_config
                deepseek_exists = True
                print("🔄 更新现有 DeepSeek 配置")
                break
        
        if not deepseek_exists:
            existing_config['llm_configs'].append(deepseek_config)
            print("➕ 添加新的 DeepSeek 配置")
        
        # 更新数据库
        config_collection.update_one(
            {'_id': existing_config['_id']},
            {'$set': {'llm_configs': existing_config['llm_configs'], 'updated_at': datetime.utcnow()}}
        )
    else:
        print("📝 创建新配置...")
        # 创建新配置
        new_config = {
            'llm_configs': [deepseek_config],
            'data_source_configs': [],
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        config_collection.insert_one(new_config)
    
    print("\n✅ DeepSeek 配置成功！")
    print(f"📝 Provider: {deepseek_config['provider']}")
    print(f"📝 Model: {deepseek_config['model_name']}")
    print(f"📝 API Key: {deepseek_config['api_key'][:20]}...")
    print(f"📝 Base URL: {deepseek_config['base_url']}")
    print(f"📝 Enabled: {deepseek_config['enabled']}")
    print(f"📝 Default: {deepseek_config['is_default']}")
    
    print("\n🎉 配置完成！请重启后端服务或刷新页面。")
    
except Exception as e:
    print(f"❌ 错误: {e}")
    print("\n💡 提示:")
    print("1. 确保 MongoDB 正在运行")
    print("2. 确保 MongoDB 不需要认证，或者配置了正确的认证信息")
    print("3. 确保数据库名称正确: tradingagents")
    sys.exit(1)
finally:
    try:
        client.close()
    except:
        pass
