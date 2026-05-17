from flask import Flask, Response, stream_with_context
import requests

app = Flask(__name__)

# 1. CUANDO PIDES UN CANAL (Ej: tu-app.vercel.app/11989)
@app.route('/<int:id_canal>')
def tunel_video(id_canal):
    # La IP original que se va a quedar bien escondida en el servidor de Vercel
    url_original = f"http://planettvweb.com:8091/PtaPta567/user8790/{id_canal}"
    
    # Nos disfrazamos de reproductor VLC legítimo ante Planet TV
    headers_vlc = {
        "User-Agent": "VLC/3.0.18 LibVLC/3.0.18",
        "Accept": "*/*"
    }
    
    try:
        # Conectamos con el flujo original de video
        req = requests.get(url_original, headers=headers_vlc, stream=True, timeout=10)
        
        # Generador para transmitir el video bit a bit (en bloques de 8KB)
        def generar_flujo():
            for chunk in req.iter_content(chunk_size=8192):
                if chunk:
                    yield chunk

        # Le respondemos a tu Roku/Cel con el video directo, sin saltos de IP
        return Response(
            stream_with_context(generar_flujo()),
            content_type="video/mp2t",
            status=200
        )
    except Exception as e:
        return f"Error en el túnel: {str(e)}", 500

# 2. CUANDO PIDES LA URL RAÍZ (Ej: tu-app.vercel.app/)
@app.route('/')
def descargar_lista():
    # Jala tu lista M3U desde tu GitHub
    url_github = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/main/DANJU80"
    try:
        res = requests.get(url_github, timeout=10)
        return Response(
            res.text,
            content_type="audio/x-mpegurl; charset=utf-8",
            headers={"Content-Disposition": "inline; filename=lista.m3u"}
        )
    except:
        return "Error al cargar la lista base", 500

# Esto es necesario para que Vercel lo detecte como Serverless
def handler(request, response):
    return app(request, response)
