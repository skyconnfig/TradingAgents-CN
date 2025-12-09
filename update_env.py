#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""更新 .env 文件中的 DeepSeek API Key"""

import os
from pathlib import Path

# 读取 .env.example
env_example = Path('.env.example')
env_file = Path('.env')

# 读取内容
with open(env_example, 'r', encoding='utf-8') as f:
    content = f.read()

# 替换 DeepSeek API Key
content = content.replace(
    'DEEPSEEK_API_KEY=your_deepseek_api_key_here',
    'DEEPSEEK_API_KEY=sk-08090b8782904fc09cee9da664a187c2'
)

# 启用 DeepSeek
content = content.replace(
    'DEEPSEEK_ENABLED=false',
    'DEEPSEEK_ENABLED=true'
)

# 写入 .env 文件
with open(env_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ .env 文件已成功更新")
print("📝 DeepSeek API Key: sk-08090b8782904fc09cee9da664a187c2")
print("🔧 DeepSeek 已启用")
