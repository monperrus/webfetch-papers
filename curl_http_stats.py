#!/usr/bin/env python3
"""
Compute per-HTTP-status-code statistics from webfetch_preprint_status.json.

Cross-tabulates the naive curl HTTP code against the agent-observed status,
showing how often HTTP 200 still results in agent failure (JS rendering, etc.)
and how often HTTP 403 still yields partial content.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

STATUS_ORDER = ["FULL_TEXT", "ABSTRACT_ONLY", "OVERFLOW", "BLOCKED", "ERROR"]
DATA_FILE = Path(__file__).parent / "webfetch_preprint_status.json"


def main() -> None:
    data = json.loads(DATA_FILE.read_text())
    results = data["results"]

    by_code: dict[int | None, list[dict]] = defaultdict(list)
    for r in results:
        by_code[r.get("curl_http_code")].append(r)

    print(f"Dataset: {DATA_FILE.name}  ({len(results)} entries)\n")
    print(f"{'HTTP':>6}  {'#':>3}  " + "  ".join(f"{s[:5]:>5}" for s in STATUS_ORDER))
    print("-" * (6 + 3 + 3 + len(STATUS_ORDER) * 8))

    for code in sorted(by_code, key=lambda x: (x is None, x or 0)):
        entries = by_code[code]
        counts = Counter(e["status"] for e in entries)
        row = "  ".join(f"{counts.get(s, 0):>5}" for s in STATUS_ORDER)
        label = str(code) if code is not None else "None"
        print(f"{label:>6}  {len(entries):>3}  {row}")

    print()
    print("Columns:", "  ".join(STATUS_ORDER))
    print()
    print("Notable:")

    # 200 but not full text
    degraded_200 = [
        r for r in by_code.get(200, []) if r["status"] not in ("FULL_TEXT", "ABSTRACT_ONLY", "OVERFLOW")
    ]
    if degraded_200:
        print(f"  HTTP 200 → agent ERROR/BLOCKED ({len(degraded_200)} URLs):")
        for r in degraded_200:
            print(f"    [{r['status']}]  {r['provider']} / {r['url_label']}  {r['url']}")

    # non-200 but agent still got content
    recovered = [
        r for r in results
        if r.get("curl_http_code", 200) not in (200,)
        and r["status"] in ("FULL_TEXT", "ABSTRACT_ONLY", "OVERFLOW")
    ]
    if recovered:
        print(f"  HTTP ≠ 200 → agent got content ({len(recovered)} URLs):")
        for r in recovered:
            print(f"    [HTTP {r['curl_http_code']}] [{r['status']}]  {r['provider']} / {r['url_label']}  {r['url']}")


if __name__ == "__main__":
    main()
