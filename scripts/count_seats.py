#!/usr/bin/env python3
"""
Count free seats on CSU library page and expose result to GitHub Actions.
"""

import datetime as dt
import os
import sys

import requests
from bs4 import BeautifulSoup

URL = "http://libzw.csu.edu.cn/web/seat2/area/95/day/2025-7-22"
CSS_SELECTOR = ".seat-usable"  # ← 若实际 HTML 不同请改这里

def main() -> None:
    try:
        r = requests.get(URL, timeout=10)
        r.raise_for_status()
    except Exception as e:
        print(f"❌ Request failed: {e}", file=sys.stderr)
        sys.exit(1)

    soup = BeautifulSoup(r.text, "html.parser")
    free_cnt = len(soup.select(CSS_SELECTOR))

    now_utc = dt.datetime.utcnow().isoformat(timespec="seconds")
    print(f"### {now_utc} UTC\nFree seats: **{free_cnt}**\n")

    # ——把结果输出给下游 step——
    output_path = os.environ.get("GITHUB_OUTPUT")
    if output_path:
        with open(output_path, "a") as f:
            f.write(f"free={free_cnt}\n")

if __name__ == "__main__":
    main()
