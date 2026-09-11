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
    # Temporary response — replace with real analysis later
    return {
        "token_address": token_address,
        "risk_score": 0,
        "risk_level": "UNKNOWN",
        "indicators": [],
        "message": "Risk analysis not implemented yet"
    }