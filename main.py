import time
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

attack_logs = []

@app.get("/", response_class=HTMLResponse)
async def dashboard_gateway():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/api/metrics")
async def fetch_live_metrics():
    return {
        "engine_status": "OPERATIONAL",
        "total_intercepted": len(attack_logs),
        "logs": attack_logs[::-1]
    }

@app.get("/api/trap/phantom-vault")
async def phantom_vault_trap(request: Request):
    client_ip = request.client.host
    headers = dict(request.headers)
    
    log_blueprint = {
        "id": f"NEXUS-{int(time.time())}",
        "timestamp": time.strftime('%H:%M:%S | %d-%m-%Y'),
        "attacker_ip": client_ip,
        "signature": headers.get("user-agent", "Hidden Identity")[:60] + "...",
        "mitigation": "CONNECTION_FROZEN_INFINITE_LOOP"
    }
    attack_logs.append(log_blueprint)

    def infinite_lock_stream():
        while True:
            yield b"CYBER_TRAP_ACTIVE_LOCK_STREAM_INFINITE..."
            time.sleep(0.001)

    return StreamingResponse(infinite_lock_stream(), media_type="text/plain")
