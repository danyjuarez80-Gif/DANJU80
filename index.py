from flask import Flask, Response, stream_with_context
import requests

app = Flask(__name__)

# 1. TUNEL DE VIDEO: Para cuando la app pide un canal numérico
@app.route('/<id_canal>')
def tunel_video(id_canal):
    # Limpiamos por si la app manda el número con ".ts" colado
    id_limpio = id_canal.replace('.ts', '')
    
    if not id_limpio.isdigit():
        return "ID de canal inválido", 400
        
    url_original = f"http://planettvweb.com:8091/PtaPta567/user8790/{id_limpio}"
    headers_vlc = {
        "User-Agent": "VLC/3.0.18 LibVLC/3.0.18",
        "Accept": "*/*"
    }
    
    try:
        req = requests.get(url_original, headers=headers_vlc, stream=True, timeout=10)
        
        def generar_flujo():
            for chunk in req.iter_content(chunk_size=8192):
                if chunk:
                    yield chunk

        return Response(
            stream_with_context(generar_flujo()),
            content_type="video/mp2t",
            status=200
        )
    except Exception as e:
        return f"Error en el túnel: {str(e)}", 500

# 2. LA RAÍZ: Aquí es donde la app descarga la lista M3U limpia
@app.route('/')
def descargar_lista():
    url_github = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/main/DANJU80"
    try:
        res = requests.get(url_github, timeout=10)
        
        # Le metemos las cabeceras pesadas de IPTV para que la app no rechace el formato
        return Response(
            res.text,
            content_type="audio/x-mpegurl; charset=utf-8",
            headers={
                "Content-Disposition": "inline; filename=lista.m3u",
                "Cache-Control": "no-cache"
            }
        )
    except:
        return "Error al cargar la lista base", 500

# Esto le ayuda a Vercel a entender la ejecución Serverless
def handler(request, response):
    return app(request, response)
