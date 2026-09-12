from datetime import datetime, timezone
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI Rug Pull Radar API",
    description="Backend API for detecting crypto token rug-pull risk",
    version="0.1.0"
)

# Allow your frontend to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict this later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "project": "AI Rug Pull Radar",
        "status": "online"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/api/risk/{token_address}")
def get_risk(token_address: str):
    chain_id = "ethereum"

    url = f"https://api.dexscreener.com/token-pairs/v1/{chain_id}/{token_address}"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    pairs = response.json()

    if not pairs:
        return {
            "token_address": token_address,
            "risk_score": None,
            "risk_level": "UNKNOWN",
            "indicators": [],
            "message": "No market data found for this token on Ethereum"
        }

    pair = max(
        pairs,
        key=lambda p: (p.get("liquidity") or {}).get("usd") or 0
    )

    liquidity_usd = (pair.get("liquidity") or {}).get("usd") or 0

    pair_created_at = pair.get("pairCreatedAt")

    if pair_created_at:
        created_time = datetime.fromtimestamp(
            pair_created_at / 1000,
            tz=timezone.utc
        )
        pool_age_days = (
            datetime.now(timezone.utc) - created_time
        ).days
    else:
        pool_age_days = None

    volume_24h_usd = (pair.get("volume") or {}).get("h24") or 0

    transactions_24h = (pair.get("txns") or {}).get("h24") or {}

    buys_24h = transactions_24h.get("buys") or 0
    sells_24h = transactions_24h.get("sells") or 0

    total_transactions = buys_24h + sells_24h

    if total_transactions > 0:
        sell_ratio = sells_24h / total_transactions
    else:
        sell_ratio = None

    if sell_ratio is None:
        sell_pressure_risk = 100
    elif sell_ratio >= 0.80:
        sell_pressure_risk = 100
    elif sell_ratio >= 0.65:
        sell_pressure_risk = 75
    elif sell_ratio >= 0.55:
        sell_pressure_risk = 40
    else:
        sell_pressure_risk = 10

    if liquidity_usd > 0:
        volume_liquidity_ratio = volume_24h_usd / liquidity_usd
    else:
        volume_liquidity_ratio = None


    if volume_liquidity_ratio is None:
        volume_risk = 100
    elif volume_liquidity_ratio > 10:
        volume_risk = 100
    elif volume_liquidity_ratio > 5:
        volume_risk = 75
    elif volume_liquidity_ratio > 2:
        volume_risk = 40
    else:
        volume_risk = 10

    if pool_age_days is None:
        pool_age_risk = 100
    elif pool_age_days < 7:
        pool_age_risk = 100
    elif pool_age_days < 30:
        pool_age_risk = 75
    elif pool_age_days < 180:
        pool_age_risk = 40
    else:
        pool_age_risk = 10

    if liquidity_usd < 10000:
        liquidity_risk = 100
    elif liquidity_usd < 50000:
        liquidity_risk = 75
    elif liquidity_usd < 250000:
        liquidity_risk = 40
    else:
        liquidity_risk = 10

    risk_score = round(
    (
        liquidity_risk
        + pool_age_risk
        + volume_risk
        + sell_pressure_risk
    ) / 4
)


    if risk_score <= 30:
        risk_level = "LOW"
    elif risk_score <= 60:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"

    
    return {
        "token_address": token_address,
        "chain": chain_id,
        "pair": pair.get("pairAddress"),
        "dex": pair.get("dexId"),
        "price_usd": pair.get("priceUsd"),
        "liquidity_usd": (pair.get("liquidity") or {}).get("usd"),
        "volume_24h_usd": (pair.get("volume") or {}).get("h24"),
        "price_change_24h_pct": (pair.get("priceChange") or {}).get("h24"),
        "pair_created_at": pair.get("pairCreatedAt"),
        "pool_age_days": pool_age_days,
        "pool_age_risk": pool_age_risk,
        "volume_liquidity_ratio": volume_liquidity_ratio,
        "volume_risk": volume_risk,
        "buys_24h": buys_24h,
        "sells_24h": sells_24h,
        "sell_ratio": sell_ratio,
        "sell_pressure_risk": sell_pressure_risk,
        "liquidity_risk": liquidity_risk,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "indicators": [],
        "message": "Risk score calculated from 4 market-based heuristic indicators"
    }