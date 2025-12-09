#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修改 .env 文件，调整 MongoDB 配置"""

from pathlib import Path

env_file = Path('.env')

# 读取内容
with open(env_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 修改 MongoDB 配置 - 移除认证
new_lines = []
for line in lines:
    if 'MONGODB_USERNAME=' in line:
        new_lines.append('MONGODB_USERNAME=\n')
    elif 'MONGODB_PASSWORD=' in line:
        new_lines.append('MONGODB_PASSWORD=\n')
    else:
        new_lines.append(line)

# 写回文件
with open(env_file, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("✅ MongoDB 配置已更新（移除认证）")
print("📝 如果 MongoDB 需要认证，请手动配置正确的用户名密码")
