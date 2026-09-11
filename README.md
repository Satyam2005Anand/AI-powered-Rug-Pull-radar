# AI-Powered Rug Pull Radar

Real-time risk scoring system that tells you how likely a token is to rug **before** you lose money.

Most people only realize a project is a scam after liquidity is pulled, the team dumps, or the contract turns into a honeypot. This tool tries to front-run that moment by combining on-chain analysis, wallet behavior, token distribution, and social/developer signals into a single rug-pull probability score.

---

## What it does

Paste a contract address (or token mint) → get:

- **Rug Probability** (0–100%)
- Breakdown by category (Contract Risk, Liquidity, Holder Distribution, Social/Team)
- Specific red flags with evidence (tx hashes, wallet addresses, etc.)
- LLM-generated explanation of *why* the score is what it is

It is **not** a guarantee. It is a high-signal early warning system.

---

## Core Features

- Smart contract static analysis (mint functions, ownership, honeypot patterns, proxies, blacklist/pause, etc.)
- Liquidity analysis (locked or not, who controls LP tokens, sudden removals)
- Holder concentration & distribution metrics
- Team/dev wallet behavior tracking
- Social + documentation signals (GitHub activity, domain age, whitepaper consistency, shill patterns)
- Multimodal risk model + anomaly detection
- Real-time or near-real-time scoring
- Clean explanation layer (not just a black-box number)

---

## How it works (high level)

1. **Ingest** – Pull contract source/bytecode, holders, liquidity, recent transactions, and available social/docs data.
2. **Analyze** – Run rule-based detectors + statistical features + anomaly scores.
3. **Score** – Weighted multimodal model produces the probability.
4. **Explain** – LLM turns the raw flags into human-readable risk factors.
5. **Output** – Score + breakdown + evidence.

---

## Tech Stack (suggested / current)

- **Backend**: Python (FastAPI / Flask)
- **On-chain**: web3.py / ethers.js + RPC providers (Alchemy, QuickNode, public RPCs)
- **Data sources**: Etherscan / Solscan / DexScreener / Birdeye / GoPlus / Honeypot.is / Dune
- **AI**: OpenAI / Claude / local LLM for explanations + optional embedding/anomaly models
- **Frontend**: Simple React / Next.js or even a Telegram bot for MVP
- **Storage** (optional): Redis for caching, Postgres for historical scores

Feel free to replace any part. The architecture is modular on purpose.

---

## Quick Start

```bash
git clone https://github.com/yourusername/rug-pull-radar.git
cd rug-pull-radar
python -m venv venv
source venv/bin/activate   # or Windows equivalent
pip install -r requirements.txt

cp .env.example .env
# fill in your API keys (Etherscan, RPC, OpenAI, etc.)

uvicorn app.main:app --reload
