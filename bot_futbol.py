import requests
import re

ARCHIVO_FIJOS = "fijos.m3u"
ARCHIVO_FINAL = "lista_danju80.m3u"
URL_BASE = "https://futbollibre.ec"

def extraer_links():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
        'Referer': URL_BASE
    }
    lista_links = []
    
    try:
        # 1. Entrar a la principal para ver todos los "Ver Canal"
        session = requests.Session()
        res = session.get(URL_BASE, headers=headers, timeout=15)
        
        # Buscamos las páginas de cada canal (ej: /embed/espn-premium/)
        canales = re.findall(r'href="(/embed/[^"]+)"', res.text)
        
        for path in canales:
            url_canal = URL_BASE + path
            try:
                # 2. "Hacemos clic" en Ver Canal
                res_canal = session.get(url_canal, headers=headers, timeout=10)
                
                # 3. Buscamos el IFRAME o el script que tiene el .m3u8 (lo que sale tras el play)
                # Buscamos el patrón source: "..." que es muy común en estos reproductores
                m3u8 = re.search(r'source:\s*"([^"]+\.m3u8[^"]*)"', res_canal.text)
                if not m3u8:
                    m3u8 = re.search(r'file:\s*"([^"]+\.m3u8[^"]*)"', res_canal.text)
                
                if m3u8:
                    link_final = m3u8.group(1)
                    # Extraemos el nombre del canal del URL para que se vea bien
                    nombre_canal = path.replace("/embed/", "").replace("-", " ").upper()
                    lista_links.append({"nombre": nombre_canal, "url": link_final})
            except:
                continue
                
        return lista_links
    except Exception as e:
        print(f"Error general: {e}")
        return []

def generar_lista():
    # Mantener tus canales del archivo fijos.m3u
    try:
        with open(ARCHIVO_FIJOS, "r", encoding="utf-8") as f:
            contenido_fijo = f.read().strip()
    except:
        contenido_fijo = "#EXTM3U"

    canales_nuevos = extraer_links()

    with open(ARCHIVO_FINAL, "w", encoding="utf-8") as f:
        f.write(contenido_fijo + "\n\n")
        f.write("# --- CANALES DE FUTBOL LIBRE DETECTADOS ---\n")
        
        if canales_nuevos:
            for c in canales_nuevos:
                f.write(f"#EXTINF:-1, [BOT] {c['nombre']}\n")
                # Importante: Pasar el User-Agent para que el reproductor no de error
                f.write(f"{c['url']}|User-Agent=Mozilla/5.0&Referer={URL_BASE}/\n")
            print(f"Se encontraron {len(canales_nuevos)} canales activos.")
        else:
            f.write("# No se detectaron transmisiones activas en este momento.\n")

if __name__ == "__main__":
    generar_lista()
