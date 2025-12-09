#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""更新 .env 文件，启用本地缓存"""

import os
from pathlib import Path

env_path = Path(".env")
key = "TA_USE_APP_CACHE"
value = "true"

print(f"Update: {env_path}")
print(f"Set: {key}={value}")

lines = []
if env_path.exists():
    with open(env_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

# 移除旧的（如果存在）
lines = [l for l in lines if not l.startswith(f"{key}=")]

# 添加新的
lines.append(f"{key}={value}\n")

with open(env_path, "w", encoding="utf-8") as f:
    f.writelines(lines)

print("✅ .env updated!")
