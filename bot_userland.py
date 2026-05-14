import requests
import re
import time

ARCHIVO_FIJOS = "fijos.m3u"
ARCHIVO_FINAL = "lista_danju80.m3u"

def infiltrar_futbol():
    enlaces = []
    # Usamos una lista de dominios espejo por si uno bloquea a GitHub
    espejos = ["https://futbollibre.ec", "https://librefutboltv.com", "https://futbollibretv.me"]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36',
        'Accept-Language': 'es-MX,es;q=0.9',
        'Referer': 'https://google.com'
    }

    with requests.Session() as s:
        for url in espejos:
            try:
                print(f"Intentando infiltracion en: {url}")
                r = s.get(url, headers=headers, timeout=15).text
                
                # Buscamos los contenedores de los reproductores
                # Estos suelen ser links que terminan en .html o tienen /embed/
                canales_raw = re.findall(r'href="([^"]*embed[^"]*)"', r)
                
                if canales_raw:
                    for path in set(canales_raw):
                        url_final = path if "http" in path else url + path
                        # Extraemos el nombre del canal del link
                        nombre = path.split('/')[-1].replace('.html', '').replace('-', ' ').upper()
                        
                        # Guardamos el link del reproductor directamente
                        # Muchas apps de IPTV pueden abrir estos links si tienen reproductor web
                        enlaces.append(f"#EXTINF:-1, [EN VIVO] {nombre}\n{url_final}")
                    
                    print(f"¡Exito! Se encontraron {len(enlaces)} canales en {url}")
                    break # Si funcionó este espejo, no probamos los demás
            except:
                continue
    return enlaces

def crear_lista():
    try:
        with open(ARCHIVO_FIJOS, "r", encoding="utf-8") as f:
            base = f.read().strip()
    except:
        base = "#EXTM3U"

    nuevos_links = infiltrar_futbol()

    with open(ARCHIVO_FINAL, "w", encoding="utf-8") as f:
        f.write(base + "\n\n")
        f.write("# --- CANALES DETECTADOS (PLAN DE EMERGENCIA) ---\n")
        if nuevos_links:
            f.write("\n".join(nuevos_links))
        else:
            f.write("# El bloqueo persiste. El sitio detecta el servidor de GitHub.\n")

if __name__ == "__main__":
    crear_lista()
