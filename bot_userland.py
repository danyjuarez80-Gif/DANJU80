import requests
import re

ARCHIVO = "lista_danju80.m3u"
FUENTES = ["https://futbollibre.ec", "https://www.rojadirectatv.tv", "https://jeinzmacias.net"]

def operacion_bypass():
    print("--- INICIANDO BYPASS DE SEGURIDAD (MODO HUMANO) ---")
    enlaces = []
    
    # Creamos una sesión para mantener las cookies como un navegador real
    sesion = requests.Session()
    sesion.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'es-MX,es;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
    })

    for url in FUENTES:
        try:
            print(f"Burlando seguridad de: {url}")
            # Primer contacto para obtener cookies de sesión
            r_base = sesion.get(url, timeout=10)
            
            # Buscamos los iframes que contienen el reproductor
            iframes = re.findall(r'src="([^"]+)"', r_base.text)
            
            for src in iframes:
                # Si el componente parece un servidor de video
                if any(x in src for x in ["embed", "stream", "player", "vagu", "cvattv"]):
                    # Entramos al componente usando las cookies obtenidas
                    link_comp = src if src.startswith('http') else url + src
                    r_comp = sesion.get(link_comp, headers={'Referer': url}, timeout=7).text
                    
                    # Limpiamos el link m3u8 escondido (eliminando el escape '\/')
                    match = re.search(r'["\'](http[^"\']+\.m3u8[^"\']*)["\']', r_comp.replace('\\/', '/'))
                    
                    if match:
                        link_final = match.group(1).split('"')[0]
                        nombre = url.split('//')[1].split('.')[0].upper()
                        # Guardamos el link con el Referer necesario para que no muera
                        enlaces.append(f"#EXTINF:-1, [BYPASS] {nombre}\n{link_final}|Referer={url}/")
                        print(f"✅ ¡DEFENSAS DERRIBADAS! Canal capturado.")
        except Exception as e:
            print(f"Falla en el punto: {url} -> {e}")
            
    return enlaces

if __name__ == "__main__":
    hacked = operacion_bypass()
    if hacked:
        with open(ARCHIVO, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n" + "\n".join(hacked))
        print(f"\nÉxito: Se rescataron {len(hacked)} flujos de video.")
    else:
        print("\nEl servidor sigue detectando al bot. Intentando nueva estrategia...")
