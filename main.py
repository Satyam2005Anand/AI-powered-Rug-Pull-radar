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
        "risk_score": None,
        "risk_level": "NOT_SCORED",
        "indicators": [],
        "message": "Real market data fetched; risk scoring not implemented yet"
    }