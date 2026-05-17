from flask import Flask, Response, stream_with_context
import requests

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    id_canal = path.replace('.ts', '').strip('/')
    
    # === PASO 1: CARGAR LA LISTA M3U ===
    if not id_canal or not id_canal.isdigit():
        url_github = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/main/DANJU80"
        try:
            res = requests.get(url_github, timeout=10)
            return Response(
                res.text,
                content_type="audio/x-mpegurl; charset=utf-8",
                headers={"Content-Disposition": "inline; filename=lista.m3u"}
            )
        except:
            return "Error al conectar con GitHub", 500

    # === PASO 2: TÚNEL USANDO EL DOMINIO ESTABLE ===
    # Cambiamos la IP muerta por el dominio que siempre responde
    url_original = f"http://planettvweb.com:8091/PtaPta567/user8790/{id_canal}"
    
    headers_vlc = {
        "User-Agent": "VLC/3.0.18 LibVLC/3.0.18",
        "Accept": "*/*"
    }
    
    try:
        # Le subimos el timeout a 15 por si el servidor de ellos tarda en despertar
        req = requests.get(url_original, headers=headers_vlc, stream=True, timeout=15)
        
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
        return f"Error en el flujo: {str(e)}", 500

def handler(request, response):
    return app(request, response)
