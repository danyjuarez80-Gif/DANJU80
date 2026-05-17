from flask import Flask, Response, stream_with_context
import requests

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    # Limpiamos la ruta por si la app manda el número con ".ts" o diagonales
    id_canal = path.replace('.ts', '').strip('/')
    
    # === PASO 1: SI LA RUTA ESTÁ VACÍA (Cargar la lista M3U) ===
    if not id_canal or not id_canal.isdigit():
        url_github = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/main/DANJU80"
        try:
            res = requests.get(url_github, timeout=10)
            # Le entregamos el texto M3U limpio a la app para que cargue las categorías
            return Response(
                res.text,
                content_type="audio/x-mpegurl; charset=utf-8",
                headers={"Content-Disposition": "inline; filename=lista.m3u"}
            )
        except:
            return "Error al conectar con GitHub", 500

    # === PASO 2: SI LLEVA EL NÚMERO DE CANAL (Hacer el Túnel Oculto) ===
    url_original = f"http://53.217.93.1:8091/PtaPta567/user8790/{id_canal}"
    headers_vlc = {
        "User-Agent": "VLC/3.0.18 LibVLC/3.0.18",
        "Accept": "*/*"
    }
    
    try:
        # Nos conectamos al servidor original en silencio
        req = requests.get(url_original, headers=headers_vlc, stream=True, timeout=10)
        
        # Transmitimos el video en bloques de 8KB directo al reproductor
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

# Necesario para la infraestructura Serverless de Vercel
def handler(request, response):
    return app(request, response)

