#!/bin/bash
# 在 Finder 里双击本文件：一定从本文件夹启动本项目预览（不会跑到别的项目）
cd "$(dirname "$0")" || exit 1
exec python3 preview.py
