import requests
import re

ARCHIVO_FIJOS = "fijos.m3u"
ARCHIVO_FINAL = "lista_danju80.m3u"
URL_BASE = "https://futbollibre.ec"

def motor_de_busqueda():
    canales = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
        'Referer': 'https://futbollibre.ec/'
    }
    
    with requests.Session() as s:
        try:
            # 1. Obtenemos la lista de los botones "Ver Canal"
            home = s.get(URL_BASE, headers=headers, timeout=10).text
            # Buscamos el patrón exacto de los botones en el HTML
            bloques = re.findall(r'href="(/embed/[^"]+)"', home)
            
            for path in set(bloques):
                url_canal = URL_BASE + path
                # 2. Entramos a la página del reproductor
                r_canal = s.get(url_canal, headers=headers, timeout=10).text
                
                # 3. RASTREO PROFUNDO:
                # Buscamos m3u8 escondidos en: source: "...", window.atob("..."), o variables JS
                # Este regex captura links directos y links con tokens
                encontrados = re.findall(r'(https?://[^\s\'"]+\.m3u8[^\s\'"]*)', r_canal)
                
                # Si no hay m3u8, buscamos el "id" del reproductor para forzar el link
                if not encontrados:
                    # A veces el link está en un iframe de otro dominio
                    iframes = re.findall(r'src="(https?://[^"]+)"', r_canal)
                    for ifr in iframes:
                        if "player" in ifr or "m3u8" in ifr:
                            r_ifr = s.get(ifr, headers={'Referer': url_canal}, timeout=5).text
                            encontrados += re.findall(r'(https?://[^\s\'"]+\.m3u8[^\s\'"]*)', r_ifr)

                for link in set(encontrados):
                    # Filtramos basura (links de imágenes o trackers que terminen en m3u8 por error)
                    if "http" in link and len(link) > 20:
                        nombre = path.replace("/embed/", "").replace("-", " ").upper()
                        canales.append({"n": nombre, "u": link})
                        
        except Exception as e:
            print(f"Error en rastreo: {e}")
            
    return canales

def actualizar():
    # Paso 1: Leer tus fijos (la lista que ya tienes)
    try:
        with open(ARCHIVO_FIJOS, "r", encoding="utf-8") as f:
            base = f.read().strip()
    except:
        base = "#EXTM3U"

    # Paso 2: El bot busca canales
    encontrados = motor_de_busqueda()

    # Paso 3: Guardar todo sin borrar lo anterior
    with open(ARCHIVO_FINAL, "w", encoding="utf-8") as f:
        f.write(base + "\n\n")
        f.write("# --- CANALES DETECTADOS POR EL BOT ---\n")
        
        if encontrados:
            for c in encontrados:
                # Agregamos la metadata para que el reproductor Android lo abra
                f.write(f"#EXTINF:-1, [BOT] {c['n']}\n")
                f.write(f"{c['u']}|User-Agent=Mozilla/5.0&Referer={URL_BASE}/\n")
            print(f"¡Éxito! Se guardaron {len(encontrados)} canales.")
        else:
            f.write("# No se detectaron links. La web podría estar usando protección anti-bot fuerte.\n")

if __name__ == "__main__":
    actualizar()
