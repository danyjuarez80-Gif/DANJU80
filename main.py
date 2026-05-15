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
    
    # CLAVE: Le añadimos 'follow_redirects=True' para que persiga el bendito error 302
    client = httpx.AsyncClient(timeout=None, follow_redirects=True)
    
    try:
        request = client.build_request("GET", target_url, headers=HEADERS)
        response = await client.send(request, stream=True)
        
        # Si aun así nos da error, que nos diga exactamente qué código da el IPTV
        if response.status_code != 200:
            await response.aclose()
            raise HTTPException(status_code=response.status_code, detail=f"IPTV respondio con codigo: {response.status_code}")
            
        return StreamingResponse(
            response.aiter_bytes(chunk_size=65536), # Duplicamos el tamaño para que no raspe el stream
            media_type="video/mp2t",
            background=response.aclose
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
