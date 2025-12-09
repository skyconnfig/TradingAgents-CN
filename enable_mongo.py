#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""更新 .env 文件，启用 MongoDB"""

import os
from pathlib import Path

env_path = Path(".env")
updates = {
    "MONGODB_ENABLED": "true",
    "TA_USE_APP_CACHE": "true"  # 再次确认
}

print(f"Update: {env_path}")

lines = []
if env_path.exists():
    with open(env_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

new_lines = []
keys_updated = []

for line in lines:
    updated = False
    for key, value in updates.items():
        if line.startswith(f"{key}="):
            new_lines.append(f"{key}={value}\n")
            keys_updated.append(key)
            updated = True
            break
    if not updated:
        # 去掉可能的乱码空行
        if line.strip():
            new_lines.append(line)

# 添加未存在的键
for key, value in updates.items():
    if key not in keys_updated:
        new_lines.append(f"{key}={value}\n")

with open(env_path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("✅ .env updated with MONGODB_ENABLED=true!")
