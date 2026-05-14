import requests
import re

ARCHIVO_FIJOS = "fijos.m3u"
ARCHIVO_FINAL = "lista_danju80.m3u"
URL_BASE = "https://futbollibre.ec"

def obtener_streams():
    enlaces = []
    # Usamos un User-Agent de Android para que la web suelte los .m3u8 más fácil
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36',
        'Referer': URL_BASE + '/'
    }
    
    with requests.Session() as s:
        try:
            # 1. Cargamos la página principal
            r = s.get(URL_BASE, headers=headers, timeout=10)
            # Buscamos los IDs de los canales que están en vivo
            ids = re.findall(r'href="/embed/([^/"]+)/"', r.text)
            
            for id_canal in set(ids):
                # 2. Entramos directo a la zona del reproductor
                url_embed = f"{URL_BASE}/embed/{id_canal}/"
                r_embed = s.get(url_embed, headers=headers, timeout=10)
                
                # 3. BUSCADOR DE ENLACES: Buscamos m3u8 o fuentes de video
                # Buscamos links que contengan .m3u8 pero que no sean imágenes
                matches = re.findall(r'(https?://[^\s\'"]+\.m3u8[^\s\'"]*)', r_embed.text)
                
                for link in matches:
                    if "http" in link and len(link) > 30:
                        enlaces.append({"n": id_canal.upper(), "u": link})
        except:
            pass
    return enlaces

def principal():
    # Carga tus canales de la imagen 83268.jpg
    try:
        with open(ARCHIVO_FIJOS, "r", encoding="utf-8") as f:
            contenido = f.read().strip()
    except:
        contenido = "#EXTM3U"

    nuevos = obtener_streams()

    with open(ARCHIVO_FINAL, "w", encoding="utf-8") as f:
        f.write(contenido + "\n\n")
        f.write("# --- CANALES EN VIVO DETECTADOS ---\n")
        
        if nuevos:
            for c in nuevos:
                # El |Referer= es lo que hace que el canal abra en tu Android
                f.write(f"#EXTINF:-1, [FUTBOL] {c['n']}\n")
                f.write(f"{c['u']}|Referer={URL_BASE}/&User-Agent=Mozilla/5.0\n")
            print(f"Se encontraron {len(nuevos)} canales.")
        else:
            # Si sigue saliendo esto, es porque no hay partidos en vivo justo ahora
            f.write("# No hay partidos en vivo en este momento en la web.\n")

if __name__ == "__main__":
    principal()
