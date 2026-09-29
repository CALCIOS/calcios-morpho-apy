#!/usr/bin/env python3
"""
CALCIOS Morpho APY Watcher — public Morpho Blue market data.
No credentials.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import requests

MORPHO_API = "https://blue-api.morpho.org/graphql"
DEFAULT_CHAIN = 4663

QUERY = """
query Markets($chainId: Int!) {
  markets(where: { chainId_in: [$chainId] }, first: 100) {
    items {
      uniqueKey
      lltv
      loanAsset { address symbol decimals }
      collateralAsset { address symbol decimals }
      state {
        supplyApy
        borrowApy
        supplyAssetsUsd
        borrowAssetsUsd
        utilization
      }
    }
  }
}
"""


def fetch_markets(chain_id: int) -> list[dict[str, Any]]:
    r = requests.post(
        MORPHO_API,
        json={"query": QUERY, "variables": {"chainId": chain_id}},
        timeout=30,
        headers={"content-type": "application/json"},
    )
    r.raise_for_status()
    data = r.json()
    if "errors" in data:
        raise SystemExit(f"Morpho API errors: {data['errors']}")
    items = data.get("data", {}).get("markets", {}).get("items") or []
    return items


def pct(x: float | None) -> str:
    if x is None:
        return "n/a"
    return f"{x * 100:.2f}%"


def main() -> None:
    p = argparse.ArgumentParser(description="CALCIOS Morpho APY watcher (public API)")
    p.add_argument("--chain-id", type=int, default=DEFAULT_CHAIN)
    p.add_argument("--json", action="store_true")
    p.add_argument("--min-supply-apy", type=float, default=None, help="Filter min supply APY (e.g. 0.01 = 1%)")
    args = p.parse_args()

    items = fetch_markets(args.chain_id)
    if args.min_supply_apy is not None:
        items = [
            m
            for m in items
            if (m.get("state") or {}).get("supplyApy") is not None
            and float(m["state"]["supplyApy"]) >= args.min_supply_apy
        ]

    if args.json:
        print(json.dumps(items, indent=2))
        return

    print(f"Chain ID: {args.chain_id}  |  Markets: {len(items)}")
    print("-" * 96)
    print(
        f"{'LOAN':<10} {'COLLATERAL':<12} {'SUPPLY APY':>12} {'BORROW APY':>12} "
        f"{'SUPPLY USD':>14} {'UTIL':>8}"
    )
    print("-" * 96)
    for m in items:
        loan = (m.get("loanAsset") or {}).get("symbol", "?")
        coll = (m.get("collateralAsset") or {}).get("symbol", "?")
        st = m.get("state") or {}
        print(
            f"{loan:<10} {coll:<12} {pct(st.get('supplyApy')):>12} "
            f"{pct(st.get('borrowApy')):>12} "
            f"{(st.get('supplyAssetsUsd') or 0):>14,.0f} "
            f"{pct(st.get('utilization')):>8}"
        )
    if not items:
        print("(no markets)")
    print("-" * 96)


if __name__ == "__main__":
    main()
