import requests
import re

ARCHIVO_FIJOS = "fijos.m3u"
ARCHIVO_FINAL = "lista_danju80.m3u"
URL_BASE = "https://futbollibre.ec"

def rastrear_network_falsa():
    # Simulamos lo que vimos en la pestaña Network
    enlaces = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': URL_BASE,
        'Accept': '*/*'
    }

    try:
        s = requests.Session()
        # 1. Obtenemos la lista de canales del home
        home = s.get(URL_BASE, headers=headers).text
        # Buscamos los IDs que usa la web (ejemplo: 'stream-1', 'espn-2')
        ids = re.findall(r'href="/embed/([^/"]+)/"', home)

        for id_canal in set(ids):
            # 2. Simulamos la petición que hace el reproductor al servidor de video
            # Muchas veces la URL es algo predecible como esto:
            url_api = f"{URL_BASE}/embed/{id_canal}/"
            r_api = s.get(url_api, headers=headers)
            
            # Buscamos el link que el reproductor "pesca" en el Network
            # Buscamos m3u8 o incluso links que vienen dentro de scripts JS
            match = re.search(r'[\'"](https?://[^\'"]+\.m3u8[^\'"]*)[\'"]', r_api.text)
            
            if match:
                link = match.group(1)
                # Si el link es relativo (ej: /live/stream.m3u8), le pegamos el dominio
                if link.startswith('/'):
                    link = "https://tu-servidor-de-video.com" + link
                
                enlaces.append({"nombre": id_canal.upper(), "url": link})
                
        return enlaces
    except:
        return []

def generar_m3u():
    # Cargar tus canales de la imagen (fijos.m3u)
    try:
        with open(ARCHIVO_FIJOS, "r", encoding="utf-8") as f:
            contenido = f.read().strip()
    except:
        contenido = "#EXTM3U"

    canales = rastrear_network_falsa()

    with open(ARCHIVO_FINAL, "w", encoding="utf-8") as f:
        f.write(contenido + "\n\n")
        f.write("# --- CANALES RASTREADOS DESDE NETWORK ---\n")
        if canales:
            for c in canales:
                f.write(f"#EXTINF:-1, [BOT] {c['nombre']}\n")
                # Agregamos los headers que vimos en Network para que no den error 403
                f.write(f"{c['url']}|Referer={URL_BASE}/&Origin={URL_BASE}\n")
        else:
            f.write("# No se detectaron peticiones m3u8 activas.\n")

if __name__ == "__main__":
    generar_m3u()
