from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import httpx

app = FastAPI()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Connection": "keep-alive"
}

@app.get("/canal/{channel_id}")
async def stream_channel(channel_id: str):
    # Tu URL original de PlanetTV
    target_url = f"http://planettvweb.com:8091/PtaPta567/user8790/{channel_id}"
    
    # Creamos el cliente con tiempos de espera infinitos para evitar micro-cortes
    client = httpx.AsyncClient(timeout=None, follow_redirects=True)
    
    try:
        request = client.build_request("GET", target_url, headers=HEADERS)
        response = await client.send(request, stream=True)
        
        if response.status_code != 200:
            await response.aclose()
            raise HTTPException(status_code=response.status_code, detail=f"Error IPTV: {response.status_code}")
            
        # ESTO ES LO QUE SOLUCIONA EL 13% EN ROKU
        custom_headers = {
            "Content-Type": "video/mp2t",              # Formato de video nativo para Roku (.ts)
            "Connection": "keep-alive",                # Mantiene el canal abierto
            "Access-Control-Allow-Origin": "*",        # Evita bloqueos de seguridad de Roku
            "Cache-Control": "no-cache, no-store",     # Obliga a la tele a renderizar en tiempo real
            "Pragma": "no-cache"
        }

        # Cambiamos el tamaño del chunk a 16KB (16384) para que el flujo sea constante y no sature la memoria de la tele
        return StreamingResponse(
            response.aiter_bytes(chunk_size=16384),
            status_code=200,
            headers=custom_headers,
            background=response.aclose
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
