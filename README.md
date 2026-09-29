# CALCIOS Morpho APY Watcher

Local Python tool to list Morpho Blue markets and supply/borrow APYs on **Robinhood Chain** (or any chain ID supported by the public Morpho API).

Part of the [CALCIOS](https://calcios.xyz/) ecosystem tooling.  
GitHub organization: [https://github.com/CALCIOS](https://github.com/CALCIOS)

## What it does

- Queries the public Morpho GraphQL API (`https://blue-api.morpho.org/graphql`)
- Prints market ID, loan/collateral assets, supply APY, borrow APY, TVL, utilization
- Default chain ID: **4663** (Robinhood Chain)
- **No wallet, no keys, no auth**

## Requirements

- Python 3.10+
- `requests`

## Installation

```bash
cd calcios-morpho-apy
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
# Robinhood Chain markets
python -m src.morpho_apy

# Another chain ID
python -m src.morpho_apy --chain-id 1

# JSON
python -m src.morpho_apy --json

# Min supply APY filter (e.g. 1%)
python -m src.morpho_apy --min-supply-apy 0.01
```

## Safety

- Public Morpho API only
- Read-only market data
- Safe for public GitHub and monitoring scripts

## License

MIT — see [LICENSE](LICENSE)
