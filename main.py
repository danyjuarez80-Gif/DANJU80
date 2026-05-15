from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import httpx

app = FastAPI()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "es-MX,es;q=0.9",
    "Connection": "keep-alive"
}

@app.get("/canal/{channel_id}")
async def stream_channel(channel_id: str):
    target_url = f"http://planettvweb.com:8091/PtaPta567/user8790/{channel_id}"
    
    # timeout=None para que Render no cuelgue la llamada si el canal tarda en responder
    client = httpx.AsyncClient(timeout=None, follow_redirects=True)
    
    try:
        request = client.build_request("GET", target_url, headers=HEADERS)
        response = await client.send(request, stream=True)
        
        if response.status_code != 200:
            await response.aclose()
            raise HTTPException(status_code=response.status_code, detail=f"IPTV Error: {response.status_code}")
            
        # CLAVE PARA ROKU: Le metemos las cabeceras que las teles exigen para flujos de video directos
        custom_headers = {
            "Content-Type": "video/mp2t", # Le avisa a la Roku que es formato TS legítimo
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*" # Evita bloqueos de seguridad del reproductor
        }

        return StreamingResponse(
            response.aiter_bytes(chunk_size=32768), # Ajustamos el buffer para que la tele llene rápido su barra de carga
            status_code=200,
            headers=custom_headers,
            background=response.aclose
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
