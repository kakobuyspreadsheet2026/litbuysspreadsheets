#!/bin/sh
# 仅服务「本目录」。推荐用 ./preview.py：随机端口 + 禁止缓存，避免总看到「上一个项目」。
# 或在 Finder 双击 Open-Preview.command
# 本脚本固定 8080，易与 litbuyplus 冲突。
cd "$(dirname "$0")" && exec python3 -m http.server 8080
