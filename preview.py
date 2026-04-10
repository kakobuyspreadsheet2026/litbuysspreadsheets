#!/usr/bin/env python3
"""
本地预览「litbuy-spreadsheet-lead」仅此项目。
- 端口由系统分配（避免 8080/8890 上旧进程仍是别的站）
- 响应带 no-cache，减少浏览器沿用旧页面
"""
from __future__ import annotations

import http.server
import os
import socketserver
import threading
import webbrowser

ROOT = os.path.dirname(os.path.abspath(__file__))


class LeadSiteHandler(http.server.SimpleHTTPRequestHandler):
    """从 ROOT 提供静态文件，并禁止缓存预览页。"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        super().end_headers()


def main() -> None:
    os.chdir(ROOT)
    title_hint = ""
    try:
        with open(os.path.join(ROOT, "index.html"), encoding="utf-8") as f:
            for line in f:
                if "<title>" in line:
                    title_hint = line.strip()[:120]
                    break
    except OSError:
        pass

    with socketserver.TCPServer(("127.0.0.1", 0), LeadSiteHandler) as httpd:
        port = httpd.server_address[1]
        url = f"http://127.0.0.1:{port}/"

        print("=" * 60)
        print("  【新项目】litbuy-spreadsheet-lead  （Litbuy 引流站 / 深色主题）")
        print(f"  固定目录: {ROOT}")
        print(f"  本次预览: {url}")
        if title_hint:
            print(f"  index 标题行: {title_hint}")
        print("  多语言: " + url + "pl/  pt/  es/  de/")
        print("=" * 60)
        print("请只使用上面「本次预览」这一行地址；不要用书签里的旧 localhost。")
        print("按 Ctrl+C 结束\n")

        threading.Timer(0.35, lambda: webbrowser.open(url)).start()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n已停止。")


if __name__ == "__main__":
    main()
