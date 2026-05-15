from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import httpx

app = FastAPI()

# El "disfraz" para que PlanetTV no te bloquee
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Connection": "keep-alive"
}

@app.get("/canal/{channel_id}")
async def stream_channel(channel_id: str):
    # Armamos la URL original que la Roku no quiere leer directo
    target_url = f"http://planettvweb.com:8091/PtaPta567/user8790/{channel_id}"
    
    client = httpx.AsyncClient(timeout=None)
    
    try:
        # Tu script en la nube se conecta al puerto 8091 de PlanetTV
        request = client.build_request("GET", target_url, headers=HEADERS)
        response = await client.send(request, stream=True)
        
        if response.status_code != 200:
            await response.aclose()
            raise HTTPException(status_code=response.status_code, detail="Error en el servidor de IPTV")
            
        # Le enviamos el video limpio a la Roku simulando que viene de Render
        return StreamingResponse(
            response.aiter_bytes(chunk_size=32768),
            media_type="video/mp2t",
            background=response.aclose
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
